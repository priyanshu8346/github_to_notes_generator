import os
import requests
from markdown2 import markdown
from weasyprint import HTML
from urllib.parse import quote
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments import highlight
from html import escape
from dotenv import load_dotenv
import re

load_dotenv()

# === CONFIG ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH")
FOLDERS_TO_INCLUDE = [folder.strip() for folder in os.getenv("FOLDERS").split(",")]

HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
FILE_EXTENSIONS = ('.md', '.cpp', '.txt')

# === GITHUB API ===
def get_github_folder_contents(owner, repo, branch, path):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ Error fetching folder contents from: {url}")
        print(f"   Error: {e}")
        return []

def download_file(url):
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"❌ Error downloading file: {url}")
        print(f"   Error: {e}")
        return ""

def process_folder(path, collected_files):
    try:
        encoded_path = quote(path)
        contents = get_github_folder_contents(GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH, encoded_path)
        if not contents:
            print(f"⚠️ Skipping empty or inaccessible folder: {path}")
            return
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith(FILE_EXTENSIONS):
                print(f"✔️ Downloading {item['path']}")
                content = download_file(item['download_url'])
                if content:
                    collected_files.append((item['path'], content))
            elif item['type'] == 'dir':
                process_folder(item['path'], collected_files)
    except Exception as e:
        print(f"❌ Error processing folder: {path}")
        print(f"   Error: {e}")

# === MARKDOWN PRE-CLEANER FOR BAD CODE BLOCKS ===
def clean_markdown_code_blocks(md_content):
    # Fix improperly written ```c++ class ... to multiline block
    md_content = re.sub(
        r"```(c\+\+|cpp)[ \t]*(?!\n)([^\n]*)",
        r"```\1\n\2",
        md_content
    )
    # Ensure closing backticks are on their own line
    md_content = re.sub(r"([^\n])```", r"\1\n```", md_content)
    return md_content

# === MARKDOWN WITH CODE HIGHLIGHTING ===
def render_markdown_with_code_highlight(md_content):
    md_content = clean_markdown_code_blocks(md_content)
    html = markdown(md_content, extras=["fenced-code-blocks"])

    def highlight_code_blocks(match):
        lang = match.group(1) or "text"
        code = match.group(2)
        try:
            lexer = get_lexer_by_name(lang)
        except:
            lexer = guess_lexer(code)
        formatter = HtmlFormatter(style="friendly", full=False, noclasses=True)
        return highlight(code, lexer, formatter)

    # Replace <pre><code class="language-xxx">...</code></pre> with highlighted blocks
    html = re.sub(
        r'<pre><code class="language-(.+?)">(.*?)</code></pre>',
        lambda m: highlight_code_blocks(m),
        html,
        flags=re.DOTALL,
    )
    return html

# === FORMAT ANY FILE TO HTML ===
def format_to_html(filename, content):
    ext = filename.split('.')[-1]
    if ext == 'md':
        return render_markdown_with_code_highlight(content)
    elif ext in ['cpp', 'c', 'py', 'js', 'java']:
        try:
            lexer = get_lexer_by_name(ext)
        except:
            lexer = guess_lexer(content)
        formatter = HtmlFormatter(style="friendly", full=False, noclasses=True)
        return highlight(content, lexer, formatter)
    else:
        return f"<pre>{escape(content)}</pre>"

# === PDF GENERATION ===
def generate_pdf(html_parts, output_file='LectureNotes.pdf'):
    try:
        combined_html = '''
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 10px;
                    margin: 20px;
                }
                h2 {
                    margin-top: 30px;
                    font-size: 13px;
                    font-weight: bold;
                    word-break: break-all;
                }
                pre, code, .highlight {
                    font-family: 'Courier New', monospace;
                    font-size: 10px;
                    background: #f4f4f4;
                    padding: 10px;
                    border-radius: 6px;
                    overflow-x: auto;
                    white-space: pre;
                    line-height: 1.4;
                    width: 100vw;
                    max-width: 100vw;
                    display: block;
                    box-sizing: border-box;
                    margin: 10px 0;
                }
                
                blockquote {
                    margin: 0;
                    padding: 0;
                    border-left: none;
                }
            </style>
        </head>
        <body>
        '''
        combined_html += ''.join(html_parts)
        combined_html += '</body></html>'
        HTML(string=combined_html).write_pdf(output_file)
        print(f"\n📄 PDF saved as: {output_file}")
    except Exception as e:
        print(f"❌ Error generating PDF.")
        print(f"   Error: {e}")

# === MAIN ===
def main():
    print("🚀 Script started")
    collected_files = []

    for folder in FOLDERS_TO_INCLUDE:
        print(f"\n📁 Processing folder: {folder}")
        process_folder(folder, collected_files)

    if not collected_files:
        print("⚠️ No files collected. Please check folder paths or network connection.")
        return

    html_parts = []
    for filename, content in collected_files:
        html = f"<h2>{filename}</h2>\n" + format_to_html(filename, content)
        html_parts.append(html)

    generate_pdf(html_parts)
    print("✅ Script finished")

if __name__ == "__main__":
    main()

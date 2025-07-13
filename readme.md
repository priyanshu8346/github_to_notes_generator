# 📝 GitHub Lecture Notes to PDF Converter

This Python script automates the process of downloading notes (Markdown, C++, text files) from specific folders in a public GitHub repository and combines them into a single, well-formatted, syntax-highlighted PDF file.

Perfect for converting structured lecture notes from a GitHub repo into a clean, printable offline PDF — especially when notes are spread across multiple folders and file types.

---

## 🚀 Features

- ✅ Download `.md`, `.cpp`, and `.txt` files from selected folders in any **public GitHub repo**
- ✅ Automatically combines and formats notes
- ✅ Supports Markdown rendering with syntax-highlighted code blocks
- ✅ Fixes common Markdown formatting issues (like broken code fences)
- ✅ Renders full-width code blocks in the final PDF
- ✅ PDF output is readable, compact, and clean
- ✅ Uses GitHub token to avoid API rate limits
- ✅ All configuration is `.env`-driven for security and flexibility

---

## 📁 Folder Structure

├── app.py # Main Python script
├── .env # Config and secret token (excluded from Git)
├── .gitignore # Ignores secrets, output, venv, etc.
├── requirements.txt # Python dependencies
└── LectureNotes.pdf # Final PDF output (auto-generated)


---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/priyanshu8346/github-notes-to-pdf.git
cd github-notes-to-pdf

##Use pip to install all required packages:

pip install -r requirements.txt
⚠️ WeasyPrint may need extra system libraries: brew install cairo pango gdk-pixbuf libffi (for macOS)

##Create a .env file
This file holds your token and settings. Create a file named .env and add the following:

GITHUB_TOKEN=your_personal_access_token
GITHUB_OWNER=Username
GITHUB_REPO=repo_name
GITHUB_BRANCH=branch name
FOLDERS=all the folders name you want to download

🔐 You can generate your token from: https://github.com/settings/tokens
You don’t need to enable any scopes — default permissions are enough for public repos.

##Run the Script
Once everything is configured, run:

python notes_to_pdf.py
If everything runs correctly, you'll see:


📁 Processing folder: 08. Intro to OOP
✔️ Downloading 08. Intro to OOP/01. Introduction.md
...
📄 PDF saved as: LectureNotes.pdf



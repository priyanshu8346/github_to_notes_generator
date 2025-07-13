

markdown
Copy
Edit
# 📝 GitHub Lecture Notes to PDF Converter

This Python script automates the process of downloading notes (`.md`, `.cpp`, `.txt` files) from specific folders in a public GitHub repository and combines them into a single, well-formatted, syntax-highlighted PDF file.

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

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/priyanshu8346/github-notes-to-pdf.git
cd github-notes-to-pdf
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
⚠️ Note for macOS:
WeasyPrint requires system libraries. Install them using:

bash
Copy
Edit
brew install cairo pango gdk-pixbuf libffi
3. Create a .env file
Create a file named .env and add the following configuration:

env
Copy
Edit
GITHUB_TOKEN=your_personal_access_token
GITHUB_OWNER=Username
GITHUB_REPO=repo_name
GITHUB_BRANCH=branch_name
FOLDERS=08. Intro to OOP,09. Operator Overloading,...
🔐 You can generate your token here: https://github.com/settings/tokens
No scopes are needed — default permissions are enough for public repos.

4. Run the script
bash
Copy
Edit
python app.py
You’ll see output like:

vbnet
Copy
Edit
📁 Processing folder: 08. Intro to OOP
✔️ Downloading 08. Intro to OOP/01. Introduction.md
...
📄 PDF saved as: LectureNotes.pdf
🛡️ Security Tip
Ensure your .env file is excluded in .gitignore:

gitignore
Copy
Edit
.env
LectureNotes.pdf
venv/
__pycache__/
🙌 Author
Priyanshu Agrawal
📧 Connect on LinkedIn
💻 GitHub Profile

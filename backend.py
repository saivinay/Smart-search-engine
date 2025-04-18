from flask import Flask, render_template, request,send_file, send_from_directory, abort
import os
import re
import hashlib
from collections import defaultdict
import PyPDF2
import docx  # pip install python-docx
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
SEARCH_DIRECTORY = '/Users/sai/Documents'  # Replace this

def extract_text_from_file(filepath):
    try:
        if filepath.lower().endswith('.pdf'):
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return '\n'.join(page.extract_text() for page in reader.pages if page.extract_text())
        elif filepath.lower().endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif filepath.lower().endswith('.docx'):
            doc = docx.Document(filepath)
            return '\n'.join([p.text for p in doc.paragraphs])
        return ""
    except Exception as e:
        print(f"[!] Error reading {filepath}: {e}")
        return ""

def extract_snippets(text, keyword, context=40, max_snippets=3):
    keyword_regex = re.compile(re.escape(keyword), re.IGNORECASE)
    snippets = []
    for match in keyword_regex.finditer(text):
        start = max(match.start() - context, 0)
        end = min(match.end() + context, len(text))
        snippet = text[start:end].replace('\n', ' ').strip()
        highlighted = keyword_regex.sub(r'<mark>\\g<0></mark>', snippet)
        snippets.append(f"...{highlighted}...")
        if len(snippets) >= max_snippets:
            break
    return snippets

def hash_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def index():
    results = []
    duplicate_files = []
    same_size_files = []

    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        filetype = request.form.get("filetype", "")

        # Add your search and logic code here that sets:
        # - results
        # - duplicate_files
        # - same_size_files

        # For now, mock up empty results (you'll have your real logic here)
        results = []
        duplicate_files = []
        same_size_files = []

    return render_template(
        "index.html",
        results=results,
        duplicate_files=duplicate_files,
        same_size_files=same_size_files
    )

def search_files(keyword, directory):
    results = []
    file_sizes = defaultdict(list)
    file_hashes = defaultdict(list)

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, directory)

            file_size = os.path.getsize(filepath)
            mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            file_sizes[file_size].append(rel_path)

            file_hash = hash_file(filepath)
            if file_hash:
                file_hashes[file_hash].append(rel_path)

            text = extract_text_from_file(filepath)
            if keyword.lower() in filename.lower() or re.search(re.escape(keyword), text, re.IGNORECASE):
                snippets = extract_snippets(text, keyword)
                results.append({
                    'filename': rel_path,
                    'content_snippet': '<br>'.join(snippets) if snippets else '(Keyword found in filename)',
                    'size': format_size(file_size),
                    'modification_date': mod_time
                })

    duplicate_files = [v for v in file_hashes.values() if len(v) > 1]
    same_size_files = [v for v in file_sizes.values() if len(v) > 1]

    return results, duplicate_files, same_size_files

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    duplicate_files = []
    same_size_files = []

    if request.method == 'POST':
        keyword = request.form['keyword']
        results, duplicate_files, same_size_files = search_files(keyword, SEARCH_DIRECTORY)

    return render_template('index.html', results=results,
                           duplicate_files=duplicate_files,
                           same_size_files=same_size_files)

@app.route('/download/<path:filename>')
def download_file(filename):
    safe_filename = os.path.normpath(filename)
    safe_path = os.path.join(SEARCH_DIRECTORY, safe_filename)
    if not os.path.isfile(safe_path):
        abort(404)
    return send_from_directory(SEARCH_DIRECTORY, safe_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

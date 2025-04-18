# Smart File Search Engine

A powerful and extensible local file search engine built with Flask. Supports multiple file types, provides content previews, identifies duplicates, and exports results.

## Features

- 🔍 Search across multiple file types: PDF, TXT, DOCX
- 📂 Recursive search through nested directories
- 🧠 Smart content previews with keyword highlighting
- 📑 Sortable search results with filename, size, and modification date
- 🧾 File type filters
- 📤 Download search results as CSV
- 🔁 Detects duplicate files based on content
- 📏 Groups files with identical sizes
- 💡 Clean and responsive UI with interactive sorting

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-file-search.git
   cd smart-file-search
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```bash
   python backend.py
   ```

5. Visit `http://localhost:5000` in your browser.

## Configuration

Set the `SEARCH_DIRECTORY` in `backend.py` to the path where your documents are stored:
```python
SEARCH_DIRECTORY = '/path/to/your/files'
```

## File Structure

```
smart-file-search/
├── backend.py           # Flask server logic
├── templates/
│   └── index.html       # HTML template with search UI
├── static/              # (optional) for JS/CSS if needed
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Dependencies

- Flask
- PyPDF2
- python-docx

Install via:
```bash
pip install Flask PyPDF2 python-docx
```

## Future Enhancements

- 📁 Drag and drop file uploads
- 🧠 Natural language understanding with AI models
- 🔒 Authentication for access control
- 📈 File indexing for faster search

## License

This project is licensed under the MIT License.

## Author

Built with ❤️ by Sai Rudrangi


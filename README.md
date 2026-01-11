# AI PDF Commander

A web application that lets you edit PDFs by chatting with them. No complex menus—just type what you want.

## How It Works

1. **User**: Uploads a file and types: "Merge these notes and remove the last page."
2. **AI (The Brain)**: Translates that English sentence into a specific command code.
3. **C++ Backend (The Muscle)**: Receives the command and edits the raw PDF file instantly.

## Features

- 🤖 **Natural Language Interface**: Simply type what you want to do in plain English
- 📄 **PDF Operations**: Merge, split, watermark, extract pages, and more
- ⚡ **Fast Processing**: C++ backend for high-performance PDF operations
- 🎨 **Modern UI**: Clean, intuitive web interface
- 🧠 **AI Command Parser**: Intelligent interpretation of user requests

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Web UI    │ ───► │  AI Parser   │ ───► │ C++ Backend │
│  (HTML/JS)  │      │   (Python)   │      │    (PDF)    │
└─────────────┘      └──────────────┘      └─────────────┘
```

### Components

1. **Frontend** (`frontend/`): Web interface for file upload and chat
2. **AI Parser** (`ai/`): Natural language command interpreter
3. **API Server** (`api/`): Flask server connecting frontend and backend
4. **C++ Backend** (`backend/`): PDF operations processor

## Installation

### Prerequisites

- Python 3.7+
- C++ compiler (g++)
- Make

### Setup

1. Clone the repository:
```bash
git clone https://github.com/arnjos096-cmyk/PDF_EDITOR.git
cd PDF_EDITOR
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Build the C++ backend:
```bash
cd backend
make
cd ..
```

## Usage

1. Start the server:
```bash
python3 api/server.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload your PDF files and start chatting!

### Example Commands

- "Merge these files"
- "Remove the last page"
- "Add watermark 'Confidential'"
- "Extract pages 1 to 5"
- "Merge these notes and remove the last page"

## Supported Operations

### Merge
Combine multiple PDF files into one.
```
"Merge these PDFs"
"Combine these files"
"Join these documents"
```

### Remove Pages
Delete specific pages from a PDF.
```
"Remove the last page"
"Delete the first 3 pages"
"Remove page 5"
```

### Watermark
Add text watermark to a PDF.
```
"Add watermark 'Confidential'"
"Watermark as 'Draft'"
"Mark as 'Internal Use Only'"
```

### Extract Pages
Extract a range of pages to a new PDF.
```
"Extract pages 1 to 5"
"Get pages 10-15"
"Save pages 2 to 8"
```

## Development

### Testing the AI Parser

```bash
python3 ai/command_parser.py
```

### Testing the C++ Backend

```bash
cd backend
./pdf_operations MERGE file1.pdf file2.pdf output.pdf
./pdf_operations WATERMARK input.pdf "Confidential" output.pdf
```

## Project Structure

```
PDF_EDITOR/
├── frontend/           # Web UI
│   └── index.html     # Main HTML page
├── ai/                # AI command parser
│   └── command_parser.py
├── api/               # Flask API server
│   └── server.py
├── backend/           # C++ PDF operations
│   ├── pdf_operations.cpp
│   └── Makefile
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Future Enhancements

- [ ] Integration with real PDF libraries (PoDoFo, QPdf)
- [ ] More advanced operations (rotate, compress, OCR)
- [ ] User authentication and file management
- [ ] Batch processing support
- [ ] Download processed files
- [ ] Command history and undo functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created with ❤️ by the AI PDF Commander team

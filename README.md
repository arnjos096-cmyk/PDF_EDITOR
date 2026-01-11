# 🤖 AI PDF Commander

**The Product:** A web app that lets you edit PDFs by chatting with them. No complex menus—just type what you want.

## 📖 The Pitch

A high-performance web application that allows users to edit PDF documents using natural language commands. Instead of navigating complex menus or paying for premium software, users simply upload a file and type instructions like "Merge these three reports and watermark the final page as 'Confidential'."

## 🎯 How It Works

1. **User:** Uploads a file and types: _"Merge these notes and remove the last page."_

2. **AI (The Brain):** Translates that English sentence into a specific command code.

3. **C++ Backend (The Muscle):** Receives the command and edits the raw PDF file instantly.

## 🏗️ Architecture

The system consists of three main components:

### 1. Frontend (Web Interface)
- **Technology:** HTML, CSS, JavaScript
- **File:** `index.html`, `styles.css`, `app.js`
- **Features:**
  - Drag-and-drop PDF upload
  - Chat-style command interface
  - Real-time command parsing
  - Visual feedback and status updates

### 2. AI Brain (Command Parser)
- **Technology:** Python
- **File:** `ai_brain.py`
- **Features:**
  - Natural language processing
  - Command translation to structured codes
  - Support for multiple operations:
    - Merge PDFs
    - Remove pages
    - Add watermarks
    - Extract pages
    - Rotate pages
    - Split PDFs
    - Compress PDFs

### 3. C++ Backend (PDF Processor)
- **Technology:** C++11
- **File:** `pdf_processor.cpp`
- **Features:**
  - High-performance PDF manipulation
  - Command execution engine
  - Multiple PDF operations support

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.6+ (for AI Brain testing)
- G++ compiler (for C++ backend)

### Quick Start

#### 1. Run the Web Interface

Simply open `index.html` in your web browser:

```bash
# On Linux/Mac
open index.html

# Or use a local server (recommended)
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

#### 2. Test the AI Brain (Python)

```bash
python3 ai_brain.py
```

This will run the command parser with example commands and show the generated command codes.

#### 3. Build and Run C++ Backend

```bash
# Build
make

# Run demo
make demo

# Clean build artifacts
make clean
```

## 💬 Example Commands

Try these natural language commands in the web interface:

- **"Merge these files"** - Combines all uploaded PDFs into one
- **"Remove the last page"** - Deletes the last page from a PDF
- **"Watermark all pages with 'Confidential'"** - Adds watermark text
- **"Extract pages 1-5"** - Pulls out specific pages
- **"Rotate all pages by 90 degrees"** - Rotates pages
- **"Split this PDF"** - Separates into individual pages
- **"Compress this file"** - Reduces PDF file size

## 📁 Project Structure

```
PDF_EDITOR/
├── index.html          # Frontend UI
├── styles.css          # Styling
├── app.js             # Frontend logic & AI integration
├── ai_brain.py        # Command parser (Python)
├── pdf_processor.cpp  # PDF operations (C++)
├── Makefile           # Build configuration
└── README.md          # This file
```

## 🔧 Command Translation Examples

| Natural Language | Command Code | Action |
|-----------------|--------------|--------|
| "Merge these files" | `CMD_MERGE_PDF 3` | Merges 3 PDFs |
| "Remove the last page" | `CMD_REMOVE_PAGE LAST` | Removes last page |
| "Watermark with 'Draft'" | `CMD_WATERMARK "Draft" ALL` | Adds watermark |
| "Extract pages 1-5" | `CMD_EXTRACT_PAGES 1-5` | Extracts pages |
| "Rotate by 90 degrees" | `CMD_ROTATE_PAGES 90 ALL` | Rotates pages |

## 🛠️ Development

### Frontend Development

The frontend is built with vanilla JavaScript for simplicity and performance. Key files:

- `index.html` - Structure and layout
- `styles.css` - Modern, responsive design with animations
- `app.js` - Command processing and UI interactions

### Backend Development

The C++ backend uses a modular design for easy extension:

```cpp
class PDFProcessor {
    bool executeCommand(const PDFCommand& cmd);
    bool mergePDFs(const PDFCommand& cmd);
    bool removePage(const PDFCommand& cmd);
    // ... other operations
};
```

### Adding New Commands

1. **Frontend (`app.js`):** Add parsing logic in `parseNaturalLanguage()`
2. **AI Brain (`ai_brain.py`):** Add new method like `_parse_newcommand()`
3. **Backend (`pdf_processor.cpp`):** Implement command in `PDFProcessor`

## 📝 Technical Notes

### Current Implementation

This is a **demonstration version** that shows the complete architecture:

- ✅ Full frontend with chat interface
- ✅ AI command parser with NLP
- ✅ C++ backend structure
- ⚠️ PDF manipulation is simulated (uses console output)

### Production Implementation

For production use, integrate real PDF libraries:

- **C++:** PoDoFo, libharu, or PDFlib
- **Python:** PyPDF2, pdfplumber, or ReportLab
- **API Layer:** Flask/FastAPI (Python) or Express (Node.js)

## 🔐 Security Considerations

- Validate all uploaded files
- Sanitize user input commands
- Implement file size limits
- Use secure file storage
- Add authentication for production use

## 🎨 Features Implemented

- ✅ Drag-and-drop file upload
- ✅ Multiple file support
- ✅ Natural language command parsing
- ✅ Real-time chat interface
- ✅ Command code generation
- ✅ Visual feedback and animations
- ✅ Responsive design
- ✅ Error handling

## 🚧 Future Enhancements

- [ ] Actual PDF manipulation (integrate PDF library)
- [ ] RESTful API layer
- [ ] User authentication
- [ ] Command history persistence
- [ ] PDF preview
- [ ] Advanced NLP with ML models
- [ ] Batch processing
- [ ] Cloud storage integration

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for easier PDF editing**

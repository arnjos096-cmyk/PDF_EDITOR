# Quick Start Guide - AI PDF Commander

Get up and running with AI PDF Commander in under 5 minutes!

## Prerequisites

Make sure you have installed:
- Python 3.7 or higher
- g++ compiler
- make

### Check Your Installation

```bash
python3 --version  # Should show 3.7+
g++ --version      # Should show any version
make --version     # Should show any version
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/arnjos096-cmyk/PDF_EDITOR.git
cd PDF_EDITOR
```

### 2. Quick Start (Easiest Method)

```bash
chmod +x start.sh
./start.sh
```

This script will:
- Install Python dependencies
- Build the C++ backend
- Start the server

### 3. Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Build C++ backend
cd backend
make
cd ..

# Start the server
python3 api/server.py
```

## Access the Application

Once the server starts, open your web browser and navigate to:

```
http://localhost:5000
```

## First Steps Tutorial

### 1. Upload PDF Files

- Click the upload area or drag and drop PDF files
- You can upload multiple files at once
- Supported format: PDF only

### 2. Try Your First Command

Click on one of the example commands or type:

```
Merge these files
```

### 3. See the Magic!

Watch as the AI:
- Understands your command
- Translates it to technical operations
- Shows you the result

## Example Commands to Try

### Basic Operations

```
Merge these files
```
Combines all uploaded PDFs into one.

```
Remove the last page
```
Deletes the last page from the first uploaded PDF.

```
Add watermark "Confidential"
```
Adds "Confidential" watermark to the PDF.

```
Extract pages 1 to 5
```
Creates a new PDF with only pages 1-5.

### Advanced Commands

```
Merge these notes and remove the last page
```
Performs two operations in sequence.

```
Combine these documents and watermark as "Draft"
```
Merges files and adds a watermark.

## Command Syntax Guide

### Merge Commands
- "Merge these files"
- "Combine these PDFs"
- "Join these documents"

### Remove Pages
- "Remove the last page"
- "Delete the first 3 pages"
- "Remove page 5"
- "Take out the last 2 pages"

### Watermark
- "Add watermark 'Confidential'"
- "Watermark as 'Draft'"
- "Mark as 'Internal Use Only'"

### Extract Pages
- "Extract pages 1 to 5"
- "Get pages 10-15"
- "Save pages 2 to 8"

## Tips for Best Results

1. **Be Specific**: Use clear commands like "Merge these files" instead of "Do something"

2. **Use Quotes for Text**: When adding watermarks, use quotes: "Add watermark 'My Text'"

3. **Upload First**: Always upload your PDF files before issuing commands

4. **One at a Time**: Start with simple commands before trying complex ones

5. **Check Examples**: Click the example tags for quick command templates

## Troubleshooting

### Server Won't Start

**Problem**: Port 5000 already in use

**Solution**: 
```bash
# Change port in api/server.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### C++ Backend Build Fails

**Problem**: g++ not found

**Solution**: Install g++
```bash
# Ubuntu/Debian
sudo apt-get install g++

# macOS
xcode-select --install

# Fedora
sudo dnf install gcc-c++
```

### Python Dependencies Error

**Problem**: Flask not found

**Solution**: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Command Not Understood

**Problem**: AI doesn't recognize your command

**Solution**: 
- Try using one of the example commands
- Check the supported commands list
- Be more specific in your phrasing

## Project Structure

```
PDF_EDITOR/
├── frontend/           # Web interface
├── ai/                 # Natural language parser
├── api/                # Flask server
├── backend/            # C++ PDF operations
├── start.sh            # Quick start script
├── requirements.txt    # Python dependencies
└── README.md           # Full documentation
```

## Testing the System

### Test AI Parser
```bash
python3 ai/command_parser.py
```

### Test C++ Backend
```bash
cd backend
./pdf_operations MERGE file1.pdf file2.pdf output.pdf
```

### Test API Server
```bash
curl http://localhost:5000/api/commands
```

## Next Steps

1. **Read the Full Documentation**: Check `README.md` for complete details

2. **Explore the Architecture**: See `ARCHITECTURE.md` for technical details

3. **Experiment**: Try different commands and combinations

4. **Provide Feedback**: Report issues or suggest features

## Common Use Cases

### Case 1: Merge Monthly Reports
```
1. Upload: jan.pdf, feb.pdf, mar.pdf
2. Command: "Merge these files"
3. Result: merged_output.pdf with all three reports
```

### Case 2: Prepare Confidential Document
```
1. Upload: report.pdf
2. Command: "Remove the last page"
3. Command: "Add watermark 'Confidential'"
4. Result: Processed document without last page and with watermark
```

### Case 3: Extract Summary Pages
```
1. Upload: full_report.pdf (100 pages)
2. Command: "Extract pages 1 to 5"
3. Result: summary.pdf with just the first 5 pages
```

## Getting Help

- **Documentation**: Read README.md and ARCHITECTURE.md
- **Issues**: Check GitHub issues for known problems
- **Examples**: Use the built-in example commands
- **Community**: Ask questions in GitHub discussions

## Performance Tips

- Keep files under 16MB for best performance
- Upload files one at a time if having issues
- Use modern browsers (Chrome, Firefox, Safari)
- Close other applications if processing is slow

## Security Notes

- Files are stored temporarily and should be deleted after processing
- Don't upload sensitive documents on shared computers
- Use HTTPS in production deployments
- Regular security updates recommended

## What's Next?

After mastering the basics, you can:
- Explore the source code
- Contribute improvements
- Suggest new features
- Deploy to production
- Integrate with your workflow

---

**Happy PDF Editing! 🎉**

For questions or feedback, visit: https://github.com/arnjos096-cmyk/PDF_EDITOR

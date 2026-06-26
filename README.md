# NeuroPDF: AI-Powered PDF Editor

NeuroPDF is a high-performance web application that allows users to edit PDF documents using natural language commands. Instead of navigating complex menus or paying for premium software, users simply upload a file and type instructions like "Redact the word Confidential" or "Add a draft watermark".

Under the hood, NeuroPDF utilizes **Google Gemini's Function Calling (Tools)** to intelligently parse user intent. It then securely routes these commands to a highly precise Python backend for execution.

## Features
- **Natural Language Editing:** Tell the AI exactly what you want to do (e.g., "Add a confidential watermark").
- **Undo/History System:** Make a mistake? Just tell the AI to "undo", "revert", or "remove", and the document safely reverts to its previous state.
- **High-Precision Backend:** Uses PyMuPDF on a Python backend for accurate physical PDF manipulation (like finding text coordinates for true text redaction).

## Tech Stack
- **Frontend:** React, Vite, Lucide Icons.
- **Backend:** Python, FastAPI, PyMuPDF (`fitz`), `@google/genai`.

## Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- A [Google Gemini API Key](https://aistudio.google.com/)

## Setup Instructions

### 1. Setup the Python AI Backend
The backend handles all LLM intent classification and PDF operations.

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your Gemini API key in your environment variables. You can do this in your terminal before running the server:
   ```bash
   export VITE_GEMINI_API_KEY="your_actual_api_key_here"
   ```
5. Start the FastAPI backend server:
   ```bash
   uvicorn main:app --reload
   ```
   *The backend will now be running on `http://localhost:8000`.*

### 2. Setup the React Frontend
The frontend provides the Chat Interface and Native PDF Viewer.

1. Open a **new** terminal window and navigate to the root directory of the project.
2. Install the Node modules:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will typically run on `http://localhost:5173`.*

## How to Use
1. Open the frontend in your browser.
2. Drag and drop a PDF file into the upload zone.
3. Once the PDF loads in the native viewer, use the chat interface on the right.
4. Try commands like:
   - *"Add a DRAFT watermark"*
   - *"Redact all mentions of [Word in your PDF]"*
   - *"Actually, remove that watermark"*
5. Click the download icon in the top right to save your modified PDF!

#!/usr/bin/env python3
"""
API Server - Integration Layer
Connects the frontend, AI brain, and C++ backend
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import json
from ai_brain import PDFCommandParser

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize AI parser
parser = PDFCommandParser()

# Upload directory
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Save file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    return jsonify({
        'success': True,
        'filename': file.filename,
        'size': os.path.getsize(filepath)
    })

@app.route('/api/parse', methods=['POST'])
def parse_command():
    """Parse natural language command"""
    data = request.json
    command = data.get('command', '')
    files = data.get('files', [])
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    # Parse with AI brain
    result = parser.parse(command, files)
    
    return jsonify(result)

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute PDF command via C++ backend"""
    data = request.json
    command_code = data.get('command_code', '')
    files = data.get('files', [])
    
    if not command_code:
        return jsonify({'error': 'No command code provided'}), 400
    
    # Build full file paths
    file_paths = [os.path.join(UPLOAD_FOLDER, f) for f in files]
    
    try:
        # Call C++ backend
        cmd = ['./pdf_processor', command_code] + file_paths
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'output': result.stdout,
                'message': 'Command executed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr,
                'message': 'Command execution failed'
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download processed PDF"""
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, as_attachment=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_brain': 'active',
        'cpp_backend': 'ready'
    })

@app.route('/')
def index():
    """Serve API information"""
    return jsonify({
        'name': 'AI PDF Commander API',
        'version': '1.0.0',
        'endpoints': {
            '/api/upload': 'POST - Upload PDF file',
            '/api/parse': 'POST - Parse natural language command',
            '/api/execute': 'POST - Execute command via C++ backend',
            '/api/download/<filename>': 'GET - Download processed PDF',
            '/api/health': 'GET - Health check'
        }
    })

if __name__ == '__main__':
    print("=" * 50)
    print("AI PDF Commander API Server")
    print("=" * 50)
    print("\nEndpoints:")
    print("  POST /api/upload     - Upload PDF file")
    print("  POST /api/parse      - Parse command")
    print("  POST /api/execute    - Execute command")
    print("  GET  /api/download   - Download result")
    print("  GET  /api/health     - Health check")
    print("\nStarting server on http://localhost:5000")
    print("=" * 50 + "\n")
    
    # Use debug=False for production, or set via environment variable
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

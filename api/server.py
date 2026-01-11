#!/usr/bin/env python3
"""
API Server - Connects the web frontend with AI parser and C++ backend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import subprocess
import json
import tempfile
from werkzeug.utils import secure_filename

# Add AI module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai'))
from command_parser import CommandParser

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
# Use environment variable or create temp directory for uploads (cross-platform)
UPLOAD_FOLDER = os.environ.get('PDF_UPLOAD_DIR', os.path.join(tempfile.gettempdir(), 'pdf_uploads'))
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

parser = CommandParser()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle PDF file uploads"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filename)
    
    if not uploaded_files:
        return jsonify({'error': 'No valid PDF files uploaded'}), 400
    
    return jsonify({
        'success': True,
        'files': uploaded_files,
        'message': f'Uploaded {len(uploaded_files)} file(s)'
    })


@app.route('/api/process', methods=['POST'])
def process_command():
    """Process natural language command"""
    data = request.json
    user_input = data.get('command', '')
    uploaded_files = data.get('files', [])
    
    if not user_input:
        return jsonify({'error': 'No command provided'}), 400
    
    # Parse natural language to commands
    parse_result = parser.parse(user_input, uploaded_files)
    
    if not parse_result['success']:
        return jsonify(parse_result), 400
    
    # Execute commands via C++ backend
    results = []
    for cmd in parse_result['commands']:
        cmd_string = parser.generate_command_string(cmd)
        
        # Call C++ backend
        backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'pdf_operations')
        
        try:
            # NOTE: Current implementation simulates execution for demo purposes.
            # TODO: For production, uncomment the actual execution code below and ensure:
            # 1. C++ backend is built (run 'make' in backend/)
            # 2. PDF library integration (PoDoFo/QPdf) is configured
            # 3. Proper error handling and timeout management
            # 4. File permissions and security are validated
            
            # SIMULATION MODE (default for demo)
            result = {
                'command': cmd['action'],
                'description': cmd['description'],
                'status': 'simulated',
                'message': f"Would execute: {cmd_string}"
            }
            
            # PRODUCTION MODE (uncomment to enable actual execution):
            # if os.path.exists(backend_path):
            #     process = subprocess.run(
            #         [backend_path] + cmd_string.split(),
            #         capture_output=True,
            #         text=True,
            #         timeout=30
            #     )
            #     result = {
            #         'command': cmd['action'],
            #         'description': cmd['description'],
            #         'output': process.stdout,
            #         'status': 'success' if process.returncode == 0 else 'error'
            #     }
            # else:
            #     result = {
            #         'command': cmd['action'],
            #         'status': 'error',
            #         'message': 'C++ backend not built. Run: cd backend && make'
            #     }
            
            results.append(result)
        except Exception as e:
            results.append({
                'command': cmd['action'],
                'status': 'error',
                'message': str(e)
            })
    
    return jsonify({
        'success': True,
        'parsed_commands': parse_result['commands'],
        'results': results
    })


@app.route('/api/commands', methods=['GET'])
def get_supported_commands():
    """Return list of supported commands"""
    return jsonify({
        'commands': [
            {
                'name': 'Merge',
                'examples': [
                    'Merge these files',
                    'Combine these PDFs',
                    'Join these documents'
                ]
            },
            {
                'name': 'Remove Pages',
                'examples': [
                    'Remove the last page',
                    'Delete the first 3 pages',
                    'Remove page 5'
                ]
            },
            {
                'name': 'Watermark',
                'examples': [
                    'Add watermark "Confidential"',
                    'Watermark as "Draft"',
                    'Mark as "Internal Use Only"'
                ]
            },
            {
                'name': 'Extract Pages',
                'examples': [
                    'Extract pages 1 to 5',
                    'Get pages 10-15',
                    'Save pages 2 to 8'
                ]
            }
        ]
    })


if __name__ == '__main__':
    print("Starting AI PDF Commander server...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

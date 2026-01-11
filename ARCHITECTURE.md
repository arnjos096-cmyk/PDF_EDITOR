# AI PDF Commander - Architecture Documentation

## System Overview

AI PDF Commander is a three-tier web application that enables users to edit PDF documents using natural language commands. The system translates human-readable instructions into executable PDF operations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                      (Web Browser)                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
                         │
┌────────────────────────▼────────────────────────────────────┐
│                     Frontend Layer                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ File Upload  │  │ Chat Interface│  │  UI Display  │     │
│  │   Component  │  │   Component   │  │  Component   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│         HTML5 + CSS3 + Vanilla JavaScript                   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         │ (JSON)
┌────────────────────────▼────────────────────────────────────┐
│                      API Server                             │
│                    (Flask/Python)                           │
│                                                              │
│  ┌───────────────┐     ┌──────────────┐                    │
│  │ Upload Handler│────►│  AI Parser   │                    │
│  │   (REST API)  │     │   Module     │                    │
│  └───────────────┘     └──────┬───────┘                    │
│                                │                             │
│  ┌───────────────┐            │                             │
│  │Command Handler│◄───────────┘                             │
│  │   (REST API)  │                                          │
│  └───────┬───────┘                                          │
└──────────┼──────────────────────────────────────────────────┘
           │ Command Strings
           │ (Text Protocol)
┌──────────▼──────────────────────────────────────────────────┐
│                    C++ Backend                              │
│                 (PDF Operations)                            │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Merge   │  │  Split   │  │Watermark │  │ Extract  │  │
│  │ Engine   │  │ Engine   │  │  Engine  │  │  Engine  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                              │
│         Command Parser & PDF Manipulation                   │
└──────────────────────────────────────────────────────────────┘
           │
           ▼
     [PDF Files]
```

## Component Details

### 1. Frontend Layer (`frontend/index.html`)

**Purpose**: Provide an intuitive user interface for PDF manipulation

**Key Features**:
- Drag-and-drop file upload
- Real-time chat interface
- Visual feedback for operations
- Example command suggestions

**Technologies**:
- HTML5 for structure
- CSS3 for styling (responsive design)
- Vanilla JavaScript for interactivity
- Fetch API for backend communication

**User Flow**:
1. User uploads PDF files via drag-drop or file picker
2. Files are displayed in the file list
3. User types natural language command
4. Command is sent to API server
5. Results are displayed in chat interface

### 2. AI Command Parser (`ai/command_parser.py`)

**Purpose**: Translate natural language into structured commands

**How It Works**:

```python
Input: "Merge these notes and remove the last page"
       ↓
Parse using regex patterns
       ↓
Identify operations: [MERGE, REMOVE_PAGES]
       ↓
Extract parameters: files, page numbers
       ↓
Output: Structured command objects
```

**Pattern Matching**:
- Uses regular expressions for command detection
- Supports multiple phrasings for same operation
- Context-aware parameter extraction

**Command Structure**:
```json
{
  "action": "MERGE",
  "params": ["file1.pdf", "file2.pdf", "output.pdf"],
  "description": "Merge uploaded PDF files"
}
```

**Supported Patterns**:

| Operation | Patterns | Parameters |
|-----------|----------|------------|
| Merge | "merge", "combine", "join" | List of files + output |
| Remove Pages | "remove", "delete" + page refs | File + page numbers |
| Watermark | "watermark", "mark as" + text | File + text + output |
| Extract | "extract", "get" + page range | File + start + end + output |

### 3. API Server (`api/server.py`)

**Purpose**: Bridge between frontend and backend components

**Endpoints**:

#### `GET /`
- Serves the main HTML interface
- Static file serving

#### `POST /api/upload`
- Handles PDF file uploads
- Validates file types
- Stores files temporarily
- Returns uploaded file list

**Request**:
```
Content-Type: multipart/form-data
files: [PDF files]
```

**Response**:
```json
{
  "success": true,
  "files": ["file1.pdf", "file2.pdf"],
  "message": "Uploaded 2 file(s)"
}
```

#### `POST /api/process`
- Receives natural language commands
- Invokes AI parser
- Executes commands via C++ backend
- Returns results

**Request**:
```json
{
  "command": "Merge these files",
  "files": ["file1.pdf", "file2.pdf"]
}
```

**Response**:
```json
{
  "success": true,
  "parsed_commands": [{...}],
  "results": [{
    "command": "MERGE",
    "status": "success",
    "message": "..."
  }]
}
```

#### `GET /api/commands`
- Returns list of supported commands
- Provides example usage

**Architecture Pattern**: 
- RESTful API design
- Stateless communication
- JSON data format

### 4. C++ Backend (`backend/pdf_operations.cpp`)

**Purpose**: Execute high-performance PDF operations

**Command Processing Flow**:
```
Command String → Parse → Validate → Execute → Return Result
```

**Command Format**:
```
ACTION param1 param2 ... output.pdf
```

**Operations**:

#### MERGE
```cpp
MERGE file1.pdf file2.pdf file3.pdf output.pdf
```
Combines multiple PDFs into a single document

#### REMOVE_PAGES
```cpp
REMOVE_PAGES input.pdf 1 5 10 output.pdf
```
Removes specified pages from PDF

#### WATERMARK
```cpp
WATERMARK input.pdf "Confidential" output.pdf
```
Adds text watermark to all pages

#### EXTRACT
```cpp
EXTRACT input.pdf 1 5 output.pdf
```
Extracts page range to new PDF

**Implementation Notes**:
- Current implementation is simplified (simulation)
- Production version would integrate libraries like:
  - PoDoFo: Full-featured PDF library
  - QPdf: PDF manipulation
  - PDFium: Rendering and editing

**Build System**:
- Makefile for compilation
- C++11 standard
- Standard library only (no dependencies for demo)

## Data Flow

### Complete Request Cycle

```
1. User Action
   └─► "Merge these files"
        ↓
2. Frontend
   └─► POST /api/process
        {command: "...", files: [...]}
        ↓
3. API Server
   └─► Parse command with AI
        ↓
4. AI Parser
   └─► Generate structured commands
        [MERGE, file1.pdf, file2.pdf, output.pdf]
        ↓
5. API Server
   └─► Execute via C++ backend
        "MERGE file1.pdf file2.pdf output.pdf"
        ↓
6. C++ Backend
   └─► Process PDF files
        Return: "SUCCESS: Merged 2 files"
        ↓
7. API Server
   └─► Return JSON response
        ↓
8. Frontend
   └─► Display result in chat
```

## Security Considerations

1. **File Upload**:
   - File type validation
   - Size limits (16MB default)
   - Secure filename sanitization

2. **Command Injection**:
   - Command parsing and validation
   - No direct shell execution
   - Parameterized operations

3. **Data Isolation**:
   - Temporary file storage
   - Session-based file management
   - Automatic cleanup

## Scalability

**Current Architecture**:
- Single-threaded Flask server
- Synchronous processing
- In-memory file handling

**Production Enhancements**:
- Load balancer for multiple instances
- Queue-based job processing (Celery, RabbitMQ)
- Distributed file storage (S3, MinIO)
- Caching layer (Redis)
- Database for job tracking

## Error Handling

**Frontend**:
- User-friendly error messages
- Network error recovery
- Input validation

**API Server**:
- HTTP status codes
- Structured error responses
- Request logging

**C++ Backend**:
- Return codes (0 = success, 1 = error)
- Error messages in output
- Graceful degradation

## Testing Strategy

**Unit Tests**:
- AI parser pattern matching
- Command generation
- C++ operation logic

**Integration Tests**:
- API endpoint testing
- End-to-end command flow
- File upload/download

**Manual Testing**:
- UI/UX validation
- Browser compatibility
- Edge cases and error scenarios

## Performance Considerations

**Bottlenecks**:
- File I/O operations
- PDF processing (merge, split)
- Network latency

**Optimizations**:
- Streaming file uploads
- Async processing for large files
- Result caching
- CDN for static assets

## Future Enhancements

1. **Advanced Operations**:
   - PDF compression
   - OCR text extraction
   - Page rotation
   - Form filling

2. **User Features**:
   - Authentication
   - File history
   - Batch processing
   - Download results

3. **AI Improvements**:
   - Machine learning for better parsing
   - Context retention across commands
   - Multi-language support
   - Command suggestions

4. **Infrastructure**:
   - Microservices architecture
   - Container deployment (Docker)
   - Kubernetes orchestration
   - Monitoring and analytics

## Dependencies

**Frontend**:
- None (vanilla JavaScript)

**Backend**:
- Python 3.7+
- Flask 2.3+
- Flask-CORS
- Werkzeug

**C++ Backend**:
- g++ compiler
- C++11 standard library
- (Future: PoDoFo, QPdf)

## Deployment

**Development**:
```bash
./start.sh
```

**Production** (recommended):
```bash
# Use gunicorn for production server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api.server:app
```

## Monitoring

**Metrics to Track**:
- Request rate
- Processing time
- Error rate
- File size distribution
- Command type distribution

**Logging**:
- Application logs
- Access logs
- Error logs
- Audit trail

## Conclusion

AI PDF Commander demonstrates a modern approach to PDF manipulation by combining natural language processing with high-performance C++ operations. The architecture is designed for extensibility and can be enhanced with real PDF libraries and additional features as needed.

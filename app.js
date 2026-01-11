// Store uploaded files
let uploadedFiles = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeChatInput();
});

// File Upload Handling
function initializeFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    const filesList = document.getElementById('filesList');
    
    Array.from(files).forEach(file => {
        if (file.type === 'application/pdf') {
            uploadedFiles.push(file);
            
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="file-info">
                    <span class="file-icon">📄</span>
                    <div>
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${formatFileSize(file.size)}</div>
                    </div>
                </div>
                <button class="remove-file" onclick="removeFile('${file.name}')">×</button>
            `;
            filesList.appendChild(fileItem);
            
            addMessage('system', `File uploaded: ${file.name} (${formatFileSize(file.size)})`);
        }
    });
}

function removeFile(fileName) {
    uploadedFiles = uploadedFiles.filter(f => f.name !== fileName);
    const filesList = document.getElementById('filesList');
    const fileItems = filesList.querySelectorAll('.file-item');
    
    fileItems.forEach(item => {
        if (item.querySelector('.file-name').textContent === fileName) {
            item.remove();
        }
    });
    
    addMessage('system', `File removed: ${fileName}`);
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Chat Input Handling
function initializeChatInput() {
    const chatInput = document.getElementById('chatInput');
    
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendCommand();
        }
    });
}

function sendCommand() {
    const chatInput = document.getElementById('chatInput');
    const command = chatInput.value.trim();
    
    if (!command) {
        return;
    }
    
    if (uploadedFiles.length === 0) {
        addMessage('error', 'Please upload at least one PDF file before sending commands.');
        return;
    }
    
    // Add user message
    addMessage('user', command);
    chatInput.value = '';
    
    // Process command
    processCommand(command);
}

function processCommand(command) {
    // AI Brain - Translate natural language to command code
    const parsedCommand = parseNaturalLanguage(command);
    
    // Add AI response
    addMessage('ai', `I understand! Processing your request...`, parsedCommand);
    
    // Simulate backend processing
    setTimeout(() => {
        executeCommand(parsedCommand);
    }, 1000);
}

function parseNaturalLanguage(text) {
    const lowerText = text.toLowerCase();
    const result = {
        action: 'UNKNOWN',
        params: {},
        commandCode: '',
        description: ''
    };
    
    // Merge detection
    if (lowerText.includes('merge') || lowerText.includes('combine') || lowerText.includes('join')) {
        result.action = 'MERGE';
        result.params.files = uploadedFiles.map(f => f.name);
        result.commandCode = `CMD_MERGE_PDF ${uploadedFiles.length} FILES`;
        result.description = `Merging ${uploadedFiles.length} PDF file(s)`;
    }
    // Remove page detection
    else if (lowerText.includes('remove') || lowerText.includes('delete')) {
        result.action = 'REMOVE_PAGE';
        
        // Detect page number or "last page"
        if (lowerText.includes('last')) {
            result.params.page = 'LAST';
            result.commandCode = 'CMD_REMOVE_PAGE LAST';
            result.description = 'Removing the last page';
        } else {
            const pageMatch = lowerText.match(/page\s+(\d+)/);
            if (pageMatch) {
                result.params.page = parseInt(pageMatch[1]);
                result.commandCode = `CMD_REMOVE_PAGE ${result.params.page}`;
                result.description = `Removing page ${result.params.page}`;
            }
        }
        
        // Detect which file
        result.params.file = uploadedFiles[0]?.name || 'document.pdf';
    }
    // Watermark detection
    else if (lowerText.includes('watermark')) {
        result.action = 'WATERMARK';
        
        // Extract watermark text
        const textMatch = lowerText.match(/['"]([^'"]+)['"]/);
        if (textMatch) {
            result.params.text = textMatch[1];
        } else {
            result.params.text = 'CONFIDENTIAL';
        }
        
        // Detect page
        if (lowerText.includes('last')) {
            result.params.page = 'LAST';
        } else if (lowerText.includes('all')) {
            result.params.page = 'ALL';
        } else {
            result.params.page = 'ALL';
        }
        
        result.commandCode = `CMD_WATERMARK "${result.params.text}" ${result.params.page}`;
        result.description = `Adding watermark "${result.params.text}" to ${result.params.page === 'ALL' ? 'all pages' : 'last page'}`;
    }
    // Extract pages
    else if (lowerText.includes('extract')) {
        result.action = 'EXTRACT';
        const rangeMatch = lowerText.match(/(\d+)-(\d+)/);
        if (rangeMatch) {
            result.params.startPage = parseInt(rangeMatch[1]);
            result.params.endPage = parseInt(rangeMatch[2]);
            result.commandCode = `CMD_EXTRACT_PAGES ${result.params.startPage}-${result.params.endPage}`;
            result.description = `Extracting pages ${result.params.startPage}-${result.params.endPage}`;
        }
    }
    // Rotate pages
    else if (lowerText.includes('rotate')) {
        result.action = 'ROTATE';
        let angle = 90;
        
        if (lowerText.includes('180')) angle = 180;
        else if (lowerText.includes('270')) angle = 270;
        
        result.params.angle = angle;
        result.commandCode = `CMD_ROTATE_PAGES ${angle}`;
        result.description = `Rotating pages by ${angle} degrees`;
    }
    
    return result;
}

function executeCommand(parsedCommand) {
    const { action, params, commandCode, description } = parsedCommand;
    
    // Display command code (what would be sent to C++ backend)
    const commandDisplay = `
        <strong>Command Translation:</strong><br>
        ${description}<br>
        <div class="command-code">${commandCode}</div>
    `;
    
    // Simulate backend execution
    if (action === 'UNKNOWN') {
        addMessage('error', 'Sorry, I couldn\'t understand that command. Try something like: "Merge these files" or "Remove the last page"');
    } else {
        addMessage('ai', commandDisplay);
        
        // Show processing status
        showStatus(`Processing: ${description}...`);
        
        // Simulate C++ backend processing
        setTimeout(() => {
            hideStatus();
            
            const resultFile = generateResultFileName(action, params);
            addMessage('system', `✅ Success! Your edited PDF is ready: <strong>${resultFile}</strong><br>
                <small>In production, this would be a download link.</small>`);
        }, 2000);
    }
}

function generateResultFileName(action, params) {
    const timestamp = new Date().getTime();
    
    switch(action) {
        case 'MERGE':
            return `merged_document_${timestamp}.pdf`;
        case 'REMOVE_PAGE':
            return `edited_${params.file}_${timestamp}.pdf`;
        case 'WATERMARK':
            return `watermarked_${timestamp}.pdf`;
        case 'EXTRACT':
            return `extracted_pages_${params.startPage}-${params.endPage}_${timestamp}.pdf`;
        case 'ROTATE':
            return `rotated_${timestamp}.pdf`;
        default:
            return `output_${timestamp}.pdf`;
    }
}

function addMessage(type, content, parsedCommand = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    let label = '';
    switch(type) {
        case 'system': label = '🤖 AI PDF Commander:'; break;
        case 'user': label = '👤 You:'; break;
        case 'ai': label = '🧠 AI Brain:'; break;
        case 'error': label = '⚠️ Error:'; break;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <strong>${label}</strong> ${content}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showStatus(message) {
    const statusSection = document.getElementById('statusSection');
    const statusContent = document.getElementById('statusContent');
    
    statusContent.innerHTML = `
        <div class="processing">
            <div class="spinner"></div>
            <span>${message}</span>
        </div>
    `;
    statusSection.style.display = 'block';
}

function hideStatus() {
    const statusSection = document.getElementById('statusSection');
    statusSection.style.display = 'none';
}

// Example commands for demonstration
function showExamples() {
    const examples = [
        "Merge these notes and remove the last page",
        "Watermark all pages with 'Confidential'",
        "Remove page 3 from document.pdf",
        "Extract pages 1-5",
        "Rotate all pages by 90 degrees"
    ];
    
    console.log('Example commands:', examples);
}

import { useState } from 'react';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import PdfPreview from './components/PdfPreview';
import { Layers } from 'lucide-react';

export default function App() {
  const [file, setFile] = useState(null);
  const [pdfHistory, setPdfHistory] = useState([]);
  const [processing, setProcessing] = useState(false);

  const pdfBytes = pdfHistory.length > 0 ? pdfHistory[pdfHistory.length - 1] : null;

  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile);
    const arrayBuffer = await selectedFile.arrayBuffer();
    setPdfHistory([new Uint8Array(arrayBuffer)]);
  };

  const handleCommand = async (command, setMessages) => {
    setProcessing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', new Blob([pdfBytes], { type: 'application/pdf' }), file.name);
      formData.append('command', command);

      const response = await fetch('http://localhost:8000/api/edit', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const actionMessage = response.headers.get('X-Action-Message') || "I processed your request.";
      const actionType = response.headers.get('X-Action-Type');

      if (actionType === 'undo') {
        if (pdfHistory.length > 1) {
          setPdfHistory(prev => prev.slice(0, prev.length - 1));
        }
      } else {
        const newArrayBuffer = await response.arrayBuffer();
        setPdfHistory(prev => [...prev, new Uint8Array(newArrayBuffer)]);
      }

      setMessages(prev => [
        ...prev, 
        { id: Date.now(), sender: 'bot', text: actionMessage }
      ]);
      
    } catch (error) {
      console.error(error);
      setMessages(prev => [
        ...prev, 
        { id: Date.now(), sender: 'bot', text: "Sorry, I couldn't connect to the AI Backend." }
      ]);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <>
      <header className="app-header glass-panel" style={{ borderRadius: 0, borderTop: 'none', borderLeft: 'none', borderRight: 'none' }}>
        <div className="app-title">
          <Layers size={28} />
          <span>NeuroPDF (Python AI Powered)</span>
        </div>
      </header>
      
      <main className="app-main">
        {!file ? (
          <FileUpload onFileSelect={handleFileSelect} />
        ) : (
          <PdfPreview file={file} pdfBytes={pdfBytes} />
        )}
        
        <ChatInterface 
          onCommandSubmit={handleCommand} 
          processing={processing} 
        />
      </main>
    </>
  );
}

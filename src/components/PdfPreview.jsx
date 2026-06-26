import { useEffect, useState } from 'react';
import { FileText, Download } from 'lucide-react';

export default function PdfPreview({ file, pdfBytes }) {
  const [blobUrl, setBlobUrl] = useState('');

  useEffect(() => {
    if (pdfBytes) {
      const blob = new Blob([pdfBytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      setBlobUrl(url);

      // Cleanup
      return () => {
        URL.revokeObjectURL(url);
      };
    }
  }, [pdfBytes]);

  const handleDownload = () => {
    if (blobUrl) {
      const a = document.createElement('a');
      a.href = blobUrl;
      const extIndex = file.name.lastIndexOf('.');
      let downloadName = file.name;
      if (extIndex > -1) {
        downloadName = file.name.substring(0, extIndex) + "_edited" + file.name.substring(extIndex);
      } else {
        downloadName += "_edited.pdf";
      }
      a.download = downloadName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  if (!file) return null;

  return (
    <div className="preview-section glass-panel pdf-preview-container animate-fade-in" style={{ display: 'flex', flexDirection: 'column' }}>
      <div className="pdf-header">
        <div className="pdf-title">
          <FileText size={20} style={{ color: 'var(--accent-color)' }} />
          {file.name}
        </div>
        <button 
          className="send-button" 
          style={{ position: 'static', transform: 'none' }} 
          title="Download Edited PDF"
          onClick={handleDownload}
        >
          <Download size={16} />
        </button>
      </div>
      
      <div className="pdf-viewer" style={{ flex: 1, padding: 0, overflow: 'hidden' }}>
        {blobUrl ? (
          <embed src={blobUrl} type="application/pdf" width="100%" height="100%" style={{ border: 'none', minHeight: '500px' }} />
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', minHeight: '500px' }}>
            Loading PDF...
          </div>
        )}
      </div>
    </div>
  );
}

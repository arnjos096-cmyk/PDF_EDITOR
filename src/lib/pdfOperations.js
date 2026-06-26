import { PDFDocument, rgb, degrees } from 'pdf-lib';

export async function processPdfCommand(fileBuffer, commandData) {
  // Load a PDFDocument from the existing PDF bytes
  const pdfDoc = await PDFDocument.load(fileBuffer);
  
  if (commandData.action === 'watermark') {
    const pages = pdfDoc.getPages();
    const text = commandData.text || 'CONFIDENTIAL';
    
    for (const page of pages) {
      const { width, height } = page.getSize();
      
      // Calculate a rough center and size based on page dimensions
      const fontSize = Math.min(width, height) / 10;
      
      page.drawText(text, {
        x: width / 2 - (fontSize * text.length) / 4, 
        y: height / 2,
        size: fontSize,
        color: rgb(0.95, 0.1, 0.1),
        opacity: 0.3,
        rotate: degrees(45),
      });
    }
  } else if (commandData.action === 'extract') {
    // Placeholder for future extraction feature
  }
  
  // Serialize the PDFDocument to bytes (a Uint8Array)
  const pdfBytes = await pdfDoc.save();
  return pdfBytes;
}

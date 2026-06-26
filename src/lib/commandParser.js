import { GoogleGenAI } from '@google/genai';

export async function parseCommand(commandStr) {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;

  if (apiKey) {
    try {
      const ai = new GoogleGenAI({ apiKey });
      const prompt = `
You are a PDF assistant. The user wants to edit a PDF.
Analyze the user's request: "${commandStr}"

Return ONLY a valid JSON object matching this schema:
{
  "action": "watermark" | "undo" | "error" | "unknown",
  "text": "The text for the watermark if applicable",
  "message": "A friendly response message telling the user what you did or why you couldn't do it."
}

If the user wants to remove, delete, or revert the previous change, action should be "undo".
If the user wants to add a watermark, action should be "watermark".
      `;
      const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: prompt,
        config: {
          responseMimeType: "application/json",
        }
      });
      
      const parsedData = JSON.parse(response.text);
      return parsedData;
    } catch (err) {
      console.error("LLM Parsing error:", err);
      // Fallback to keyword matching below
    }
  }

  // Fallback keyword parser
  const lowerCmd = commandStr.toLowerCase();
  
  if (lowerCmd.includes('remove') || lowerCmd.includes('undo') || lowerCmd.includes('delete') || lowerCmd.includes('revert')) {
    return {
      action: 'undo',
      message: "I've reverted the previous change for you."
    };
  }

  if (lowerCmd.includes('watermark')) {
    let text = 'CONFIDENTIAL';
    if (lowerCmd.includes('draft')) text = 'DRAFT';
    if (lowerCmd.includes('approved')) text = 'APPROVED';
    if (lowerCmd.includes('secret')) text = 'TOP SECRET';
    
    return { 
      action: 'watermark', 
      text, 
      message: `I have successfully added a '${text}' watermark to the document.` 
    };
  }
  
  if (lowerCmd.includes('redact')) {
    return { 
      action: 'error', 
      message: 'Redaction currently requires a backend OCR service to identify text coordinates, which is not set up in this demo.' 
    };
  }
  
  if (lowerCmd.includes('merge')) {
    return {
      action: 'error',
      message: 'To merge, please upload multiple files first. (This feature is coming soon!)'
    }
  }
  
  return { 
    action: 'unknown', 
    message: `I'm not sure how to apply "${commandStr}". Try asking me to "Add a confidential watermark".` 
  };
}

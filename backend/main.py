from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from agent import process_command
from tools.pdf_tools import redact_text, add_watermark
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For demo purposes, allow all
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Action-Message"]
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.post("/api/edit")
async def edit_pdf(file: UploadFile = File(...), command: str = Form(...)):
    # Save incoming file
    file_id = str(uuid.uuid4())
    input_path = f"uploads/{file_id}.pdf"
    output_path = f"outputs/{file_id}_out.pdf"
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Get tool decision from Gemini
    decision = process_command(command)
    
    if decision["action"] == "redact_text":
        redact_text(input_path, output_path, decision["args"]["text_to_redact"])
        return FileResponse(output_path, headers={"X-Action-Message": f"Successfully redacted '{decision['args']['text_to_redact']}'."})
        
    elif decision["action"] == "add_watermark":
        add_watermark(input_path, output_path, decision["args"]["watermark_text"])
        return FileResponse(output_path, headers={"X-Action-Message": f"Added watermark '{decision['args']['watermark_text']}'."})
        
    elif decision["action"] == "undo":
        return FileResponse(input_path, headers={"X-Action-Message": "I have reverted the previous change.", "X-Action-Type": "undo"})
        
    elif decision["action"] == "error":
        # Return original with error message
        return FileResponse(input_path, headers={"X-Action-Message": f"Error: {decision['message']}"})
        
    else:
        # Just return the original if we don't know what to do
        return FileResponse(input_path, headers={"X-Action-Message": decision.get("message", "I am not sure how to do that. Try asking to redact or watermark.")})

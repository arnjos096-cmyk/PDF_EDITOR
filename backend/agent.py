import os
from google import genai
from google.genai import types

def process_command(command: str):
    # Initializes Gemini client and configures tools
    api_key = os.environ.get("VITE_GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    
    if not api_key:
        return {"action": "error", "message": "Gemini API key is missing. Please set VITE_GEMINI_API_KEY in your environment."}
        
    client = genai.Client(api_key=api_key)
    
    # Declare functions that Gemini can call
    tools = [
        types.Tool(function_declarations=[
            types.FunctionDeclaration(
                name="redact_text",
                description="Use this when the user wants to redact, hide, or black out specific text or words in the document.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "text_to_redact": types.Schema(type=types.Type.STRING, description="The exact text string to redact from the document."),
                    },
                    required=["text_to_redact"]
                )
            ),
            types.FunctionDeclaration(
                name="add_watermark",
                description="Use this when the user wants to add a watermark, stamp, or overlay text on the document.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "watermark_text": types.Schema(type=types.Type.STRING, description="The text to use as the watermark (e.g., 'CONFIDENTIAL', 'DRAFT')."),
                    },
                    required=["watermark_text"]
                )
            ),
            types.FunctionDeclaration(
                name="undo",
                description="Use this when the user asks to undo, remove, delete, or revert the previous change they made.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={}
                )
            )
        ])
    ]
    
    # Call Gemini model
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=command,
            config=types.GenerateContentConfig(
                tools=tools,
                temperature=0.1
            )
        )
        
        # Check if Gemini decided to call a function
        if response.function_calls:
            fc = response.function_calls[0]
            if fc.name == "redact_text":
                return {"action": "redact_text", "args": fc.args}
            elif fc.name == "add_watermark":
                return {"action": "add_watermark", "args": fc.args}
            elif fc.name == "undo":
                return {"action": "undo"}
                
        # If it just returned text, no tool was needed or matched
        return {"action": "unknown", "message": response.text}
        
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {"action": "error", "message": f"Failed to parse command with Gemini: {str(e)}"}

import os
import json
from openai import OpenAI

def process_command(command: str):
    # Initialize OpenAI client (this works for OpenAI, Groq, local Ollama, etc.)
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", None)
    
    if not api_key:
        return {"action": "error", "message": "API key is missing. Please set OPENAI_API_KEY in your environment."}
        
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Standard OpenAI JSON Schema for tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "redact_text",
                "description": "Use this when the user wants to redact, hide, or black out specific text or words in the document.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text_to_redact": {
                            "type": "string",
                            "description": "The exact text string to redact from the document."
                        }
                    },
                    "required": ["text_to_redact"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_watermark",
                "description": "Use this when the user wants to add a watermark, stamp, or overlay text on the document.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "watermark_text": {
                            "type": "string",
                            "description": "The text to use as the watermark (e.g., 'CONFIDENTIAL', 'DRAFT')."
                        }
                    },
                    "required": ["watermark_text"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "undo",
                "description": "Use this when the user asks to undo, remove, delete, or revert the previous change they made.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a highly capable PDF editing assistant."},
                {"role": "user", "content": command}
            ],
            tools=tools,
            temperature=0.1
        )
        
        message = response.choices[0].message
        
        # Check if the LLM decided to call a function
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            
            # The arguments come back as a JSON string
            args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
            
            if function_name == "redact_text":
                return {"action": "redact_text", "args": args}
            elif function_name == "add_watermark":
                return {"action": "add_watermark", "args": args}
            elif function_name == "undo":
                return {"action": "undo"}
                
        # If no tool was called
        return {"action": "unknown", "message": message.content or "I couldn't figure out which tool to use."}
        
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return {"action": "error", "message": f"Failed to parse command: {str(e)}"}

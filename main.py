from fastapi import FastAPI, HTTPException, Query
import httpx
import re
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

# Load environment variables
load_dotenv()

app = FastAPI(title="WhatsApp Messaging API")

# Configuration - these would typically come from environment variables
WHAPI_API_URL = os.getenv("WHAPI_API_URL", "https://gate.whapi.cloud/messages/text")
WHAPI_TOKEN = os.getenv("WHAPI_TOKEN")

class MessageResponse(BaseModel):
    success: bool
    message: str
    message_id: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "WhatsApp Messaging API is running. Use /send_message endpoint to send messages."}

@app.get("/send_message", response_model=MessageResponse)
async def send_message(
    phone_number: str = Query(..., description="Recipient's phone number with country code, e.g., 61371989950"),
    message: str = Query("Hello, this message was sent via API!", description="Message to send")
):
    # Validate phone number format (simple validation)
    if not re.match(r"^\d{10,15}$", phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format. Please provide 10-15 digits only.")

    # Check if token is configured
    if not WHAPI_TOKEN:
        raise HTTPException(status_code=500, detail="WhatsApp API token is not configured. Please set the WHAPI_TOKEN environment variable.")

    # Construct the WhatsApp API request
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "to": phone_number,
        "body": message
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(WHAPI_API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get("id", "unknown")
                return MessageResponse(
                    success=True,
                    message="Message sent successfully!",
                    message_id=message_id
                )
            else:
                # Try to get error message from response
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", str(error_data))
                except:
                    error_msg = f"Error status code: {response.status_code}"
                
                raise HTTPException(status_code=response.status_code, detail=f"WhatsApp API error: {error_msg}")
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with WhatsApp API: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
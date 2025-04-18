# WhatsApp Messaging FastAPI

A FastAPI application that integrates with WhApi.cloud API to send WhatsApp messages.

## Features

- RESTful API endpoint for sending WhatsApp messages
- Phone number validation
- Customizable message content
- Error handling
- Environment-based configuration

## Prerequisites

- Python 3.8+
- WhApi.cloud API token

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd whatsapp-fastapi
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your WhatsApp API credentials:
   ```
   WHAPI_API_URL=https://gate.whapi.cloud/messages/text
   WHAPI_TOKEN=your_token_here
   ```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

After starting the server, view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Send WhatsApp Message

```
GET /send_message?phone_number=61371989950&message=Hello%20World
```

Parameters:
- `phone_number`: The recipient's phone number with country code, without any symbols or spaces
- `message` (optional): The text message to send (defaults to "Hello, this message was sent via API!")

Response:
```json
{
  "success": true,
  "message": "Message sent successfully!",
  "message_id": "message_id_value"
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- `400`: Invalid phone number format
- `401/403`: Authentication issues with WhatsApp API
- `500`: Server errors or communication issues with WhatsApp API

## Production Deployment

For production deployments:
1. Use a proper WSGI server (e.g., Gunicorn)
2. Set up SSL/TLS for secure communication
3. Implement proper logging
4. Consider using a reverse proxy like Nginx

Example production deployment:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
import json
from twilio.request_validator import RequestValidator
from config import Config

app = FastAPI()
config = Config()

@app.post("/sms")
async def receive_sms(request: Request):
    """
    Receives SMS messages from Twilio and validates the request using Twilio's signature.
    """
    # Validate the Twilio signature
    validator = RequestValidator(config.twilio_auth_token)
    data = await request.form()
    request_valid = validator.validate(
        str(request.url),
        data,
        request.headers.get('X-Twilio-Signature', '')
    )

    if not request_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request signature")

    # Log the message to the console
    body = data.get('Body')
    sender = data.get('From')
    print(f"Received SMS from {sender}: {body}")

    return Response()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
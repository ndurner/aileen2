from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
from twilio.request_validator import RequestValidator
from config import Config
from webagent import WebAgent
import mylog

app = FastAPI()
config = Config()
mylog.setup_logging()
logger = mylog.getLogger(__name__)

@app.post("/sms")
async def receive_sms(request: Request):
    validator = RequestValidator(config.twilio_auth_token)
    data = await request.form()
    request_valid = validator.validate(
        str(request.url),
        data,
        request.headers.get('X-Twilio-Signature', '')
    )

    if not request_valid:
        logger.error("Invalid request signature")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request signature")

    body = data.get('Body')
    sender = data.get('From')
    logger.debug(f"Received SMS from {sender}: {body}")

    profile_id = sender
    profile = config.user_profiles.get(profile_id)
    if profile is None:
        logger.warning(f"No profile found for sender: {sender}")
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    agent = WebAgent()
    agent.start(body, profile)

    return Response()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
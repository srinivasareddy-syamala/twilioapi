from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = FastAPI()


# -----------------------------
# ROOT ROUTE (Health Check)
# -----------------------------
@app.get("/")
def home():
    return {"message": "Doctor VoIP Server is running successfully"}


# -----------------------------
# INCOMING CALL HANDLER
# -----------------------------
@app.post("/voice")
async def voice():
    response = VoiceResponse()

    gather = Gather(
        num_digits=1,
        action="/process-price",
        method="POST"
    )

    gather.say(
        "Welcome to City Hospital. "
        "Press 1 for Basic consultation costing 500 rupees. "
        "Press 2 for Standard consultation costing 1000 rupees. "
        "Press 3 for Premium consultation costing 2000 rupees."
    )

    response.append(gather)

    # If no input
    response.redirect("/voice")

    return Response(content=str(response), media_type="application/xml")


# -----------------------------
# PROCESS PRICE SELECTION
# -----------------------------
@app.post("/process-price")
async def process_price(request: Request):
    form = await request.form()
    digit = form.get("Digits")

    price_map = {
        "1": ("Basic", 500),
        "2": ("Standard", 1000),
        "3": ("Premium", 2000)
    }

    consultation, price = price_map.get(digit, ("Basic", 500))

    response = VoiceResponse()

    response.say(
        f"You selected {consultation} consultation costing {price} rupees. "
        "Your appointment request has been recorded. "
        "Our staff will contact you shortly. Thank you."
    )

    response.hangup()

    return Response(content=str(response), media_type="application/xml")


# -----------------------------
# LOCAL RUN (Optional)
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

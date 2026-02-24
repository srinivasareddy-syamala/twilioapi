from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = FastAPI()

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
        "Press 1 for Basic consultation. "
        "Press 2 for Standard consultation. "
        "Press 3 for Premium consultation."
    )

    response.append(gather)

    return Response(content=str(response), media_type="application/xml")


@app.post("/process-price")
async def process_price(request: Request):
    form = await request.form()
    digit = form.get("Digits")

    price_map = {
        "1": "Basic",
        "2": "Standard",
        "3": "Premium"
    }

    selected_price = price_map.get(digit, "Basic")

    response = VoiceResponse()
    response.say(f"You selected {selected_price} consultation. Thank you.")

    return Response(content=str(response), media_type="application/xml")

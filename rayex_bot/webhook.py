# rayex_bot/webhook.py
from flask import Flask, request
from .engine import RayexBot
from .models import Session, State
from .config import Messages

app = Flask(__name__)
bot = RayexBot()

# In-memory storage for sessions (simulated database)
# key: user_id (phone number), value: Session object
sessions = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Endpoint for WhatsApp Webhook.
    Assumes standard form-encoded data typically sent by Twilio for WhatsApp.
    If using Meta direct API, payload parsing would differ (JSON).
    """
    # 1. Get incoming message details
    # For Twilio: 'From' is sender, 'Body' is message text
    incoming_msg = request.values.get('Body', '').strip()
    sender_id = request.values.get('From', '')

    if not sender_id:
        return "No Sender ID", 400

    # 2. Retrieve or Create Session
    if sender_id not in sessions:
        sessions[sender_id] = Session(user_id=sender_id)
        # If new session, we might want to greet them regardless of input?
        # Or just process their input.
        # If they say "Hi", process_message handles it.
        # But wait, initially new session is WAITING_FOR_MENU.
        # If they say "Hi", that's invalid input for menu.
        # We should check if it's potentially a greeting to START.
        # Hack: If new session, force Greeting response first?
        # Or let the engine handle "reset" logic.
        
    session = sessions[sender_id]
    
    # 3. Process Message
    response_text = bot.process_message(session, incoming_msg)

    # 4. Return TwiML response (for Twilio)
    # Simple XML format
    from twilio.twiml.messaging_response import MessagingResponse
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp)

if __name__ == "__main__":
    # To run: python3 -m rayex_bot.webhook
    app.run(port=5000, debug=True)

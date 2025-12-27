# Rayex WhatsApp Bot

A Python-based WhatsApp bot for Rayex Global, facilitating Naira ↔ RMB and USDT ↔ RMB exchanges.

## Features
-   **Conversation Flow**: Guided interaction for FX exchanges and business support.
-   **State Management**: Ensures users provide all necessary details before confirmation.
-   **Configurable Rates**: easy-to-update exchange rates.
-   **WhatsApp Integration**: Flask-based webhook ready for Twilio.

## Setup

1.  **Install Python 3.x**
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running Locally

### 1. CLI Simulation (Testing)
Run the bot in your terminal to test the logic without WhatsApp:
```bash
python3 main.py
```
Type `reset` to restart the session.

### 2. WhatsApp Webhook (Development)
Start the Flask server to receive real WhatsApp messages (requires Twilio):
```bash
python3 -m rayex_bot.webhook
```
The server runs on `http://127.0.0.1:5000`.

## Twilio Integration Guide

To connect this bot to WhatsApp, you need a **Twilio Account**.

### Prerequisites
1.  **Twilio Account SID & Auth Token**: Found in your Twilio Console.
2.  **WhatsApp Sender**:
    -   **Sandbox**: Great for testing. Activate it in `Messaging > Try it out > Send a WhatsApp message`.
    -   **Production**: Requires Business Verification and enabling a Twilio number for WhatsApp.

### Connecting the Webhook
Twilio needs to communicate with your running bot. Since your bot is running locally, you need a tunnel (like **ngrok**) to expose it to the internet.

1.  **Install ngrok**: I have downloaded it to your project folder.
2.  **Start ngrok**:
    ```bash
    ./ngrok config add-authtoken <YOUR_AUTHTOKEN>
    ./ngrok http 127.0.0.1:5000
    ```
    Copy the "Forwarding" URL (e.g., `https://a1b2-c3d4.ngrok-free.app`).
3.  **Configure Twilio**:
    -   Go to **Messaging > Settings > WhatsApp Sandbox Settings** (or your active number settings).
    -   In the **"When a message comes in"** field, paste your ngrok URL appended with `/webhook`.
    -   Example: `https://a1b2-c3d4.ngrok-free.app/webhook`
    -   Set method to **POST**.
    -   Save settings.

### Configuration
Rates can be updated in `rayex_bot/config.py`:
```python
class Rates:
    NGN_TO_RMB_RATE = 230.0
    USDT_TO_RMB_RATE = 7.20
```

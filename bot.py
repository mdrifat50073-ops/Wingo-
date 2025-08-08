import time
import requests
import threading
from flask import Flask, request

BOT_TOKEN = '7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4'
CHAT_ID = '6848807471'
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = Flask(__name__)
running = False
base_period = None

def predict_signal(period):
    number = period % 10
    return '⬆️ Big' if number >= 5 else '⬇️ Small'

def send_message(text):
    requests.post(API_URL, data={'chat_id': CHAT_ID, 'text': text})

def signal_loop():
    global running, base_period
    while running:
        signal = predict_signal(base_period)
        send_message(f"🎯 Period: {base_period} → {signal}")
        base_period += 1
        time.sleep(60)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global running, base_period
    data = request.get_json()
    if not data or 'message' not in data:
        return "ok"

    msg = data['message']
    text = msg.get('text', '')
    chat_id = msg['chat']['id']

    if str(chat_id) != CHAT_ID:
        return "unauthorized"

    if text == '/start':
        if not running and base_period is not None:
            running = True
            threading.Thread(target=signal_loop).start()
            send_message("✅ Bot started.")
        else:
            send_message("⚠️ Send a period number first or bot already running.")

    elif text == '/stop':
        running = False
        send_message("🛑 Bot stopped.")

    elif text.isdigit() and len(text) >= 5:
        base_period = int(text)
        send_message(f"📌 Base period set: {base_period}\nNow send /start to begin.")

    else:
        send_message("❓ Unknown command.")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

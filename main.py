import time
import requests
from flask import Flask, request
import threading

app = Flask(__name__)

BOT_TOKEN = "7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4"
CHAT_ID = "6848807471"
running = False
period = 11111

def predict(period):
    digit = int(str(period)[-1])
    size = "Big" if digit in [1, 4, 5, 7, 8] else "Small"
    color = "Red" if digit in [1, 4, 7] else "Green" if digit in [2, 5, 8] else "Violet"
    return size, color

def generate_message(period):
    size, color = predict(period)
    return f"""🎲 Number Prediction for Hgnice-App

🎯 Period: {period}
🎰 Result: {size}
💠 Colour: {color}"""

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def signal_loop():
    global running, period
    while running:
        msg = generate_message(period)
        send_message(msg)
        period += 1
        time.sleep(60)

@app.route('/start', methods=['GET'])
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=signal_loop).start()
        send_message("✅ Bot Started")
    return "Bot Started"

@app.route('/stop', methods=['GET'])
def stop():
    global running
    running = False
    send_message("🛑 Bot Stopped")
    return "Bot Stopped"

@app.route('/', methods=['GET'])
def home():
    return "Bot is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

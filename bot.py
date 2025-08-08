import time
import requests

BOT_TOKEN = '7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4'
CHAT_ID = '6848807471'

def generate_signal(period):
    if period % 3 == 0:
        return '🔴 Red'
    elif period % 2 == 0:
        return '🟢 Green'
    else:
        return '🟣 Violet'

def send_signal():
    while True:
        current_time = int(time.time())
        period = current_time // 60
        signal = generate_signal(period)
        message = f"🕐 Period: {period}\n🎯 Signal: {signal}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': message}
        requests.post(url, data=payload)
        time.sleep(60)

send_signal()

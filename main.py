from flask import Flask, request
import requests
import os

app = Flask(__name__)

# حتماً این متغیر محیطی روی Render ست شده باشه
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("data:", data)  # برای دیباگ

    if not data or "message" not in data:
        return "No message", 400

    message = data["message"]
    chat_id = message["chat"]["id"]

    text = message.get("text", "").strip()

    # فقط زمانی که کاربر /start زد جواب بده
    if text == "/start":
        send_message(chat_id, "سلام 👋 خوبی؟ چخبر؟")

    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print("Telegram error:", response.text)
    except Exception as e:
        print("خطا در ارسال پیام:", e)

# مسیر Health Check
@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request
import requests
import os

app = Flask(__name__)

# گرفتن توکن از محیط امن
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

# پیام خوش‌آمد
WELCOME_MESSAGE = "سلام 👋\nخوبی؟\nچخبر؟\nچیکارا می‌کنی؟"

# تابع ارسال پیام به تلگرام
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در ارسال پیام: {e}")

# روت اصلی برای دریافت پیام از تلگرام
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "❌ No data received", 400

    message = data.get("message")
    if not message:
        return "❌ No message found", 400

    chat = message.get("chat")
    text = message.get("text")

    if chat and text:
        chat_id = chat.get("id")
        if text.strip() == "/start":
            send_message(chat_id, WELCOME_MESSAGE)
        else:
            send_message(chat_id, "فعلاً فقط به /start جواب می‌دم 😉")
    return "✅ OK", 200

# اجرای اپلیکیشن
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

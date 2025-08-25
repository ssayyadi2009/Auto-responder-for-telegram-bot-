from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "No message", 400

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").strip()

    if text == "/start":
        message = """سلام ✌️
خوبی؟ چه خبر؟ 😎
من ربات @shervin_sayyadi2009 هستم 🤖
فقط وقتی لازم باشه میام کمک در حالت عادی هم کاربرد دیگه‌ای ندارم ❌"""
        send_message(chat_id, message)
    # پیام‌های دیگر نادیده گرفته می‌شوند

    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": text})
        if response.status_code != 200:
            print("Telegram error:", response.text)
    except Exception as e:
        print("خطا در ارسال پیام:", e)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

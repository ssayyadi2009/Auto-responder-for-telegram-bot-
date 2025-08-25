from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

# پیام اصلی اولین /start
FIRST_MESSAGE = """سلام ✌️
خوبی؟ چه خبر؟ 😎
من ربات @shervin_sayyadi2009 هستم 🤖
فقط وقتی لازم باشه میام کمک در حالت عادی هم کاربرد دیگه‌ای ندارم ❌"""

# پیام‌های دفعات بعدی /start
NEXT_MESSAGES = [
    "عه 😳 بازم /start؟!\nمن که خاموش نشده بودم 😂",
    "هی رفیق! فکر کردی با /start روشن میشم؟\nمن همیشه آن‌لاینم 😎",
    "باز زدی /start؟\nبابا من آماده‌م از قبل 🤖",
    "عه، مگه دفعه پیش بدرقه‌ت نکردم؟ 🤔",
    "/start زدی؟/n یعنی دلت برام تنگ شده 😏",
    "بازم سلام 😅\nسلامای قبلی کم نبود؟",
    "عههه 😳 هنوز اینجایی؟\nمن فکر کردم رفتی!",
    "اوووهو! چند بار می‌خوای منو استارت کنی؟ 🚀",
    "داداش من خودکار روشن میشم، لازم نیس هی استارت بدی 😅",
    "فکر کردی باتری دارم که باید روشنم کنی؟ 🤨",
    "باور کن من Reset نمی‌خوام 😅",
    "اینو چندمین بار زدی؟\nبذار یه دفترچه بیارم بشمرم 📒😂",
    "باشه، استارت شدیم دوباره!\nولی خب… از قبل استارت بودم 😎",
    "/start زدی؟\nخب من که همین‌جا بودم 😎",
    "هی رفیق! استارت زدی یعنی حوصله‌ت سر رفته؟ 🤔",
    "باز سلام کردی؟\nسلامِ قبلی هنوز گرمه 🌞",
    "عه!\nمگه خاموشم کرده بودی؟ 🤖",
    "/start پشت /start؟\nمی‌خوای رکوردم بزنیم؟ 🏆",
    "سلام دوباره 👋\nاین دیگه چندمین باره؟",
    "من حس می‌کنم داری منو تست می‌کنی 😏",
    "بازم سلام، من خسته نمی‌شم ولی تو چی؟ 😂",
    "ههه! بازم استارت؟\nبذار قهوه‌مو بخورم بعد ✋☕",
    "باز اومدی؟\nخب خوش اومدی دیگه ✨",
    "عه داداش، من ۲۴/۷ روشنم، لازم نیس استارت بزنی 😅",
    "تو رکورد زدی توی سلام کردن 😂",
    "یه روز بدون استارت هم امتحان کن،\nقول میدم هنوز باشم 😎",
    "باشه، دوباره سلام!\nولی دیگه تکرار نشه ها 😏"
]

# پیام‌های برگشتی بعد از بلاک و آنبلاک
RETURN_MESSAGES = [
    "برگشتی؟ فکر کردی با بلاک منو فراری دادی؟ 😂",
    "وااای! برگشتی! بلاک و آنبلاک شدنت یه تست شجاعت بود؟ 😏",
    "عههه! برگشتی 😎\nمن که همیشه چشمام بهت بود 👀",
    "باز اومدی؟\nپس بلاک فقط یه حقه کوچیک بود، نه؟ 😅",
    "ههه! برگشتی!\nخب حالا دیگه می‌خوای چیکار کنی؟ 🤖",
    "آها برگشتی!\nپس بلاک فقط یه امتحان کوچیک بود 😅",
    "عه! دوباره برگشتی,\nفکر کردی بدون من می‌تونی؟ 😎",
    "باز اومدی!\nخب خوش اومدی، آماده‌م واسه گپ زدن 😏"
]

# وضعیت هر کاربر
# {chat_id: {"index": n, "blocked": True/False, "return_index": m}}
user_data = {}

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "No message", 400

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").strip()

    if text == "/start":
        info = user_data.get(chat_id, {"index": 0, "blocked": False, "return_index": 0})

        if info["blocked"]:
            # پیام برگشتی چرخه‌ای
            msg_index = info["return_index"]
            send_message(chat_id, RETURN_MESSAGES[msg_index])
            info["return_index"] = (msg_index + 1) % len(RETURN_MESSAGES)
        else:
            if chat_id not in user_data:
                # اولین بار → پیام اصلی
                send_message(chat_id, FIRST_MESSAGE)
            else:
                idx = info["index"]
                send_message(chat_id, NEXT_MESSAGES[idx])
                info["index"] = (idx + 1) % len(NEXT_MESSAGES)

        user_data[chat_id] = info

    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": text})
        if response.status_code == 200:
            return True
        else:
            # اگر بلاک بود
            if "bot was blocked by the user" in response.text.lower():
                if chat_id in user_data:
                    user_data[chat_id]["blocked"] = True
            print("Telegram error:", response.text)
            return False
    except Exception as e:
        print("خطا در ارسال پیام:", e)
        return False

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

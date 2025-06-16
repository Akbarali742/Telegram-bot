import requests
import time

TOKEN = "8072672790:AAH0vfEJMn34EBKWnsluaeKkmRSSiMx6h90"
CHANNEL_USERNAME = "@music_phonk_uz"  # kanal username'si

API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    res = requests.get(url, params=params)
    return res.json()["result"]

def send_message(chat_id, text, reply_markup=None):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(url, data=data)

def check_subscription(user_id):
    url = f"{API_URL}/getChatMember"
    params = {"chat_id": CHANNEL_USERNAME, "user_id": user_id}
    res = requests.get(url, params=params).json()
    status = res.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

def main():
    print("Bot ishlayapti...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                user_id = message["from"]["id"]

                if check_subscription(user_id):
                    send_message(chat_id, "✅ Kanalga obuna bo‘lgansiz. Botdan foydalanishingiz mumkin.")
                else:
                    keyboard = {
                        "inline_keyboard": [
                            [{"text": "🔔 Obuna bo‘lish", "url": f"https://t.me/{CHANNEL_USERNAME[1:]}"}]
                        ]
                    }
                    send_message(chat_id, "❌ Iltimos, botdan foydalanish uchun kanalga obuna bo‘ling.", reply_markup=str(keyboard).replace("'", '"'))
        time.sleep(1)

if __name__ == "__main__":
    main()
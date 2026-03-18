import os
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates():
    # Fetch unread messages from the bot
    response = requests.get(f"{URL}/getUpdates").json()
    return response.get("result", [])

def send_message(chat_id, text):
    # Send a reply back to Telegram
    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def mark_as_read(update_id):
    # This clever trick tells Telegram we processed the message, 
    # so it deletes it from the queue and doesn't run it again next time!
    requests.get(f"{URL}/getUpdates?offset={update_id + 1}")

updates = get_updates()

if not updates:
    print("No new messages. Going back to sleep.")

for update in updates:
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        command = update["message"]["text"]
        update_id = update["update_id"]

        print(f"Received command: {command}")

        # --- DO YOUR ACTUAL WORK HERE ---
        # (e.g., trigger a database backup, scrape a website, run tests)
        
        reply_text = f"✅ GitHub successfully executed your command: '{command}'"
        
        # --------------------------------

        send_message(chat_id, reply_text)
        mark_as_read(update_id)

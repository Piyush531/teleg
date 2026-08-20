import os
import threading
from flask import Flask
import telebot

# Keep-alive server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask).start()

# Telegram Bot Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_CHAT_ID = os.environ.get("YOUR_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['text'])
def forward_text(message):
    if str(message.chat.id) != str(YOUR_CHAT_ID):
        sender = message.from_user.first_name
        bot.send_message(
            YOUR_CHAT_ID, 
            f"📩 *New message from {sender}:*\n\n{message.text}", 
            parse_mode="Markdown"
        )

@bot.message_handler(content_types=['photo'])
def forward_photo(message):
    if str(message.chat.id) != str(YOUR_CHAT_ID):
        sender = message.from_user.first_name
        photo_id = message.photo[-1].file_id 
        caption = message.caption if message.caption else "No caption provided."

        bot.send_photo(
            YOUR_CHAT_ID, 
            photo=photo_id, 
            caption=f"📸 *Photo from {sender}:*\n\n{caption}", 
            parse_mode="Markdown"
        )

bot.infinity_polling(timeout=10, long_polling_timeout=5)

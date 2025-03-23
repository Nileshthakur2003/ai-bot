import os
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler
from ai import get_ai_response  # Import AI logic from ai.py
from db import store_userdata_log
from dotenv import load_dotenv
import asyncio
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)

async def start(update, context):
    """
    Handles the /start command.
    """
    await update.message.reply_text(
        "🤖 Bot Activated! Welcome to the AI-Powered Community Bot By System Altruism! 🎉\nUse /ai <your message> to get AI responses."
    )

async def ai_command(update, context):
    """
    Handles the /ai command and generates AI responses.
    """
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if len(context.args) == 0:
        await update.message.reply_text("⚠️ Please provide a message. Usage: /ai <your message>")
        return

    user_message = " ".join(context.args)
    reply = get_ai_response(user_message)
    store_userdata_log(user_id, user_name, user_message, reply)

    chunks = [reply[i:i + 4096] for i in range(0, len(reply), 4096)]
    for chunk in chunks:
        await update.message.reply_text(chunk)





def run_telegram_bot():
    """
    Initializes and runs the Telegram bot in a new thread with an asyncio event loop.
    """
    # Create a new asyncio event loop for the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Initialize the Telegram bot application
    application = ApplicationBuilder().token(os.getenv("BOT_KEY")).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ai", ai_command))

    print("Telegram bot is polling...")

    # Run the bot with the new event loop
    loop.run_until_complete(application.run_polling())

@app.route("/")
def home():
    return "AI-Powered Community Bot is running!"

if __name__ == "__main__":
    # Run the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()

    # Run the Flask app
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
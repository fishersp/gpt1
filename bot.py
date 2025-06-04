import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting message."""
    await update.message.reply_text("Hello! I'm your digital twin. Ask me anything.")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward the user's message to OpenAI and send back the response."""
    user_message = update.message.text
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
        )
        reply = completion.choices[0].message.content
    except Exception as exc:
        reply = f"Error: {exc}"
    await update.message.reply_text(reply)

def main() -> None:
    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
        raise EnvironmentError("Missing TELEGRAM_BOT_TOKEN or OPENAI_API_KEY")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    app.run_polling()

if __name__ == "__main__":
    main()

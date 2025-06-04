import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

openai.api_key = OPENAI_API_KEY

# Keep conversation history per user
conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting message."""
    await update.message.reply_text(
        "Hello! I'm your ChatGPT twin. Send me a message and I'll respond."
    )

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward the user's message to OpenAI and send back the response."""
    user_id = update.effective_user.id
    history = conversations.setdefault(
        user_id,
        [
            {
                "role": "system",
                "content": "You are a digital twin of the user's ChatGPT profile.",
            }
        ],
    )
    history.append({"role": "user", "content": update.message.text})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
        )
        reply = completion.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
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

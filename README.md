# gpt1

This repository contains a simple Telegram bot that forwards user messages to the OpenAI ChatGPT API. The bot behaves like a digital twin of your ChatGPT profile and remembers each user's conversation.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the following environment variables with your credentials:
   - `TELEGRAM_BOT_TOKEN` – token for your Telegram bot
   - `OPENAI_API_KEY` – API key for OpenAI

3. Run the bot:
   ```bash
   python bot.py
   ```

The bot listens for messages and replies using ChatGPT. Each chat maintains its own history so the responses stay in context.

## Troubleshooting
If you see a `SyntaxError` mentioning lines like `index 000000...` when running `bot.py`,
you may have copied diff markers instead of the actual code. Download the raw
`bot.py` file from this repository to avoid that issue.

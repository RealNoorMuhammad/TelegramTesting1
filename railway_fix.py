#!/usr/bin/env python3
"""
Railway Fix - Simple Bot that Works
"""

import os
import asyncio
import logging
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'polyfocus-bot',
        'version': '1.0.0',
        'bot': '@Polymarketsolanabot'
    })

@app.route('/')
def root():
    return jsonify({
        'message': 'PolyFocus Bot is running!',
        'bot': '@Polymarketsolanabot',
        'link': 'https://t.me/Polymarketsolanabot'
    })

async def telegram_bot():
    """Simple Telegram bot."""
    try:
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
        from telegram.constants import ParseMode
        
        token = os.getenv('TELEGRAM_BOT_TOKEN', '7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E')
        
        app = Application.builder().token(token).build()
        
        async def start(update, context):
            await update.message.reply_text(
                "🚀 **PolyFocus 1.0.0**\n\n"
                "Welcome to your Polymarket trading bot!\n\n"
                "Send any text to search for markets.",
                parse_mode=ParseMode.MARKDOWN
            )
        
        async def handle_text(update, context):
            text = update.message.text
            await update.message.reply_text(
                f"🔍 **Search Results for '{text}'**\n\n"
                f"Mock market: {text.title()}\n"
                f"YES: 0.65 | NO: 0.35\n"
                f"Volume: $1.2M",
                parse_mode=ParseMode.MARKDOWN
            )
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        logger.info("Starting Telegram bot...")
        await app.run_polling()
        
    except Exception as e:
        logger.error(f"Bot error: {e}")

def run_bot():
    """Run bot in background."""
    import threading
    def start_bot():
        asyncio.run(telegram_bot())
    
    thread = threading.Thread(target=start_bot)
    thread.daemon = True
    thread.start()
    return thread

if __name__ == '__main__':
    print("🚀 Starting PolyFocus Bot...")
    print("🤖 Bot: @Polymarketsolanabot")
    
    # Start bot
    run_bot()
    
    # Start web server
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

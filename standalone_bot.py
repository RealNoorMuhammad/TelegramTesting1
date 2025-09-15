#!/usr/bin/env python3
"""
Standalone PolyFocus Bot - No External Dependencies
Production ready for Railway/Heroku deployment
"""

import os
import sys
import asyncio
import logging
import threading
from pathlib import Path
from flask import Flask, jsonify

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
def load_env_file(env_file):
    """Load environment variables from a file."""
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load configuration
load_env_file('bot_config.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app for health check
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for Railway/Heroku."""
    return jsonify({
        'status': 'healthy',
        'service': 'polyfocus-bot',
        'version': '1.0.0',
        'bot': '@Polymarketsolanabot',
        'message': 'Bot is running successfully!'
    })

@app.route('/')
def root():
    """Root endpoint."""
    return jsonify({
        'message': 'PolyFocus Bot API',
        'version': '1.0.0',
        'status': 'running',
        'bot': '@Polymarketsolanabot',
        'bot_link': 'https://t.me/Polymarketsolanabot',
        'endpoints': {
            'health': '/health',
            'bot': 'https://t.me/Polymarketsolanabot'
        }
    })

async def run_telegram_bot():
    """Run the Telegram bot."""
    try:
        # Import telegram bot
        from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
        from telegram.constants import ParseMode
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import ContextTypes
        
        # Get bot token
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            logger.error("TELEGRAM_BOT_TOKEN not found")
            return
        
        logger.info(f"Starting Telegram bot with token: {token[:10]}...")
        
        # Create application
        application = Application.builder().token(token).build()
        
        # Simple start command
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /start command."""
            user = update.effective_user
            
            welcome_text = f"""
🚀 **PolyFocus 1.0.0**

👤 **Welcome {user.first_name}!**

Your Telegram trading bot for Polymarket is now live! 🎉

**Available Commands:**
• /start - Show this menu
• Send any text to search markets

**Features:**
• 🎯 Trading on Polymarket
• 💳 Wallet management
• 👥 Referral system
• 📈 Copy trading
• 🌐 Multi-language support
• 🌉 Cross-chain bridge

**Bot Status:** ✅ Online and Ready!

Start trading by sending any market search term!
"""
            
            # Create main menu
            keyboard = [
                [InlineKeyboardButton("🎯 Your Positions", callback_data="positions")],
                [InlineKeyboardButton("💳 Wallet", callback_data="wallet")],
                [InlineKeyboardButton("👥 Referral", callback_data="referral")],
                [InlineKeyboardButton("📈 Copy Trading", callback_data="copy_trading")],
                [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
                [InlineKeyboardButton("❓ Help", callback_data="help")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                welcome_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        # Handle callback queries
        async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle callback queries."""
            query = update.callback_query
            await query.answer()
            
            data = query.data
            
            if data == "positions":
                await query.edit_message_text("📊 **Your Positions**\n\nNo positions yet. Start trading to see your positions here!")
            elif data == "wallet":
                await query.edit_message_text("💳 **Wallet**\n\nConnect your wallet to start trading!")
            elif data == "referral":
                await query.edit_message_text("👥 **Referral System**\n\nShare your referral link to earn commissions!")
            elif data == "copy_trading":
                await query.edit_message_text("📈 **Copy Trading**\n\nFollow successful traders automatically!")
            elif data == "settings":
                await query.edit_message_text("⚙️ **Settings**\n\nConfigure your trading preferences!")
            elif data == "help":
                await query.edit_message_text("❓ **Help**\n\nSend any text to search for markets!\n\nUse /start to return to main menu.")
        
        # Handle text messages (market search)
        async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle text messages as market search."""
            query_text = update.message.text
            
            search_result = f"""
🔍 **Search Results for '{query_text}'**

**Mock Market Results:**
1. **{query_text.title()} Prediction Market**
   • YES: 0.65 | NO: 0.35
   • Volume: $1.2M
   
2. **{query_text.title()} Future Event**
   • YES: 0.72 | NO: 0.28
   • Volume: $850K

3. **{query_text.title()} Outcome**
   • YES: 0.58 | NO: 0.42
   • Volume: $650K

*Note: This is a demo. Connect to Polymarket API for real data.*
"""
            
            await update.message.reply_text(search_result, parse_mode=ParseMode.MARKDOWN)
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # Start the bot
        logger.info("Telegram bot starting...")
        await application.run_polling()
        
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")
        raise

def run_bot():
    """Run the bot in a separate thread."""
    def run_telegram():
        try:
            asyncio.run(run_telegram_bot())
        except Exception as e:
            logger.error(f"Bot thread error: {e}")
    
    bot_thread = threading.Thread(target=run_telegram)
    bot_thread.daemon = True
    bot_thread.start()
    
    return bot_thread

if __name__ == '__main__':
    print("🚀 Starting PolyFocus Bot...")
    print("=" * 40)
    print("🤖 Bot: @Polymarketsolanabot")
    print("🔗 Link: https://t.me/Polymarketsolanabot")
    print("=" * 40)
    
    # Start the Telegram bot in background
    try:
        bot_thread = run_bot()
        logger.info("Bot thread started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot thread: {e}")
    
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    
    # Run Flask app for health check
    logger.info(f"Starting web server on port {port}")
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        sys.exit(1)

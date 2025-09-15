#!/usr/bin/env python3
"""
GL Testing Bot - Simple Working Version
Bot: @GLtestingsolbot
Token: 8368872230:AAFp_NMUW9Ym1qS_qqhHtvJmOIObZr8l_GE
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
        'service': 'gl-testing-bot',
        'version': '1.0.0',
        'bot': '@GLtestingsolbot'
    })

@app.route('/')
def root():
    return jsonify({
        'message': 'GL Testing Bot is running!',
        'bot': '@GLtestingsolbot',
        'link': 'https://t.me/GLtestingsolbot'
    })

async def telegram_bot():
    """GL Testing Telegram bot."""
    try:
        from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
        from telegram.constants import ParseMode
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        # Use the new bot token
        token = '8368872230:AAFp_NMUW9Ym1qS_qqhHtvJmOIObZr8l_GE'
        
        app = Application.builder().token(token).build()
        
        async def start(update, context):
            """Handle /start command."""
            user = update.effective_user
            
            welcome_text = f"""
🚀 **GL Testing Bot 1.0.0**

👤 **Welcome {user.first_name}!**

Your Telegram bot for Polymarket trading is now live! 🎉

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
        
        async def handle_callback(update, context):
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
        
        async def handle_text(update, context):
            """Handle text messages as market search."""
            text = update.message.text
            
            search_result = f"""
🔍 **Search Results for '{text}'**

**Mock Market Results:**
1. **{text.title()} Prediction Market**
   • YES: 0.65 | NO: 0.35
   • Volume: $1.2M
   
2. **{text.title()} Future Event**
   • YES: 0.72 | NO: 0.28
   • Volume: $850K

3. **{text.title()} Outcome**
   • YES: 0.58 | NO: 0.42
   • Volume: $650K

*Note: This is a demo. Connect to Polymarket API for real data.*
"""
            
            await update.message.reply_text(search_result, parse_mode=ParseMode.MARKDOWN)
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        logger.info("Starting GL Testing Bot...")
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
    print("🚀 Starting GL Testing Bot...")
    print("🤖 Bot: @GLtestingsolbot")
    print("🔗 Link: https://t.me/GLtestingsolbot")
    print("=" * 50)
    
    # Start bot
    run_bot()
    
    # Start web server
    port = int(os.getenv('PORT', 8000))
    print(f"🌐 Web server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

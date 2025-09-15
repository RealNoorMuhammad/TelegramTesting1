#!/usr/bin/env python3
"""
Status check script for PolyFocus Bot
"""

import os
import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_bot_status():
    """Check if the bot is running."""
    print("🔍 Checking PolyFocus Bot Status...")
    print("=" * 40)
    
    # Load environment variables
    def load_env_file(env_file):
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    load_env_file('bot_config.env')
    
    # Check configuration
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token and token != 'your_telegram_bot_token_here':
        print(f"✅ Bot Token: {token[:10]}...")
    else:
        print("❌ Bot Token not configured")
        return False
    
    # Check database
    db_path = "data/polymarket_bot.db"
    if os.path.exists(db_path):
        print(f"✅ Database: {db_path} exists")
    else:
        print(f"⚠️  Database: {db_path} not found (will be created on first run)")
    
    # Check logs
    if os.path.exists("logs"):
        print("✅ Logs directory exists")
    else:
        print("⚠️  Logs directory not found")
    
    print("\n📱 Bot Information:")
    print(f"🤖 Bot Username: @Polymarketsolanabot")
    print(f"🔗 Bot Link: https://t.me/Polymarketsolanabot")
    
    print("\n🚀 To start the bot:")
    print("1. Run: python start_bot.py")
    print("2. Go to: https://t.me/Polymarketsolanabot")
    print("3. Send: /start")
    
    print("\n📋 Available Commands:")
    print("• /start - Initialize bot and show main menu")
    print("• Send any text to search for markets")
    print("• Use menu buttons for all features")
    
    return True

if __name__ == '__main__':
    check_bot_status()

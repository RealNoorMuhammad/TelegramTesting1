#!/usr/bin/env python3
"""
Startup script for PolyFocus Bot
This script loads the configuration and starts the bot
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from bot_config.env
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

# Now import and run the bot
if __name__ == '__main__':
    print("🚀 Starting PolyFocus Bot...")
    print("=" * 40)
    
    # Check if required environment variables are set
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ TELEGRAM_BOT_TOKEN not found in bot_config.env")
        print("Please make sure your bot_config.env file has the correct token.")
        sys.exit(1)
    
    if not os.getenv('ENCRYPTION_KEY'):
        print("❌ ENCRYPTION_KEY not found in bot_config.env")
        sys.exit(1)
    
    print("✅ Configuration loaded successfully!")
    print(f"🤖 Bot Token: {os.getenv('TELEGRAM_BOT_TOKEN')[:10]}...")
    print(f"🔑 Encryption Key: {os.getenv('ENCRYPTION_KEY')[:10]}...")
    print("\n🚀 Starting bot...")
    
    try:
        from main import main
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        sys.exit(1)

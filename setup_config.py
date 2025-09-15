#!/usr/bin/env python3
"""
Setup configuration script for PolyFocus Bot
This script helps you configure the bot with proper environment variables
"""

import os
import secrets
import string
from pathlib import Path

def generate_encryption_key():
    """Generate a secure 32-character encryption key."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def create_env_file():
    """Create .env file with configuration."""
    print("🔧 Setting up PolyFocus Bot Configuration")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Generate encryption key
    encryption_key = generate_encryption_key()
    
    # Get user input
    print("\n📝 Please provide the following information:")
    print("(Press Enter to use default values where applicable)\n")
    
    telegram_token = input("🤖 Telegram Bot Token: ").strip()
    if not telegram_token:
        print("❌ Telegram Bot Token is required!")
        return
    
    polymarket_api_key = input("📊 Polymarket API Key (optional): ").strip()
    lifi_api_key = input("🌉 LI.FI API Key (optional): ").strip()
    google_translate_key = input("🌐 Google Translate API Key (optional): ").strip()
    
    webhook_url = input("🔗 Webhook URL (optional): ").strip()
    if not webhook_url:
        webhook_url = "https://yourdomain.com/webhook"
    
    # Create .env content
    env_content = f"""# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={telegram_token}
TELEGRAM_WEBHOOK_URL={webhook_url}

# Database Configuration
DATABASE_URL=sqlite:///./data/polymarket_bot.db
ENCRYPTION_KEY={encryption_key}

# Polymarket API Configuration
POLYMARKET_GAMMA_API_URL=https://gamma-api.polymarket.com
POLYMARKET_DATA_API_URL=https://data-api.polymarket.com
POLYMARKET_CLOB_API_URL=https://clob.polymarket.com
POLYMARKET_API_KEY={polymarket_api_key or 'your_polymarket_api_key_here'}

# LI.FI Bridge API
LIFI_API_URL=https://li.quest/v1
LIFI_API_KEY={lifi_api_key or 'your_lifi_api_key_here'}

# Google Translate API
GOOGLE_TRANSLATE_API_KEY={google_translate_key or 'your_google_translate_api_key_here'}

# WebSocket Configuration
WEBSOCKET_URL=wss://clob.polymarket.com/ws

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ Configuration saved to .env file!")
        print(f"🔑 Generated encryption key: {encryption_key}")
        
        # Show next steps
        print("\n🚀 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run locally: python main.py")
        print("3. Or deploy with Docker: docker-compose up -d")
        print("\n📱 To start the bot:")
        print("1. Find your bot on Telegram")
        print("2. Send /start command")
        print("3. Follow the menu options")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def check_requirements():
    """Check if all requirements are met."""
    print("\n🔍 Checking requirements...")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required. Current version:", sys.version)
        return False
    else:
        print("✅ Python version:", sys.version.split()[0])
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    else:
        print("✅ requirements.txt found")
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ main.py not found!")
        return False
    else:
        print("✅ main.py found")
    
    return True

def main():
    """Main setup function."""
    print("🚀 PolyFocus Bot Setup")
    print("=" * 30)
    
    if not check_requirements():
        print("\n❌ Setup failed. Please check the requirements.")
        return
    
    print("\n✅ All requirements met!")
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    print("✅ Created data and logs directories")
    
    # Create .env file
    create_env_file()

if __name__ == '__main__':
    main()

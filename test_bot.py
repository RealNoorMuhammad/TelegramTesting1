#!/usr/bin/env python3
"""
Test script for PolyFocus Bot
This script tests the bot configuration and basic functionality
"""

import os
import sys
from pathlib import Path

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

load_env_file('bot_config.env')

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from database import init_db
        print("✅ Database module imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from bot.handlers import BotHandlers
        print("✅ Bot handlers imported successfully")
    except Exception as e:
        print(f"❌ Bot handlers import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test bot configuration."""
    print("\n🔧 Testing configuration...")
    
    from config import Config
    
    if not Config.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        return False
    else:
        print(f"✅ Telegram Bot Token: {Config.TELEGRAM_BOT_TOKEN[:10]}...")
    
    if not Config.ENCRYPTION_KEY:
        print("❌ ENCRYPTION_KEY not set")
        return False
    else:
        print(f"✅ Encryption Key: {Config.ENCRYPTION_KEY[:10]}...")
    
    print(f"✅ Database URL: {Config.DATABASE_URL}")
    print(f"✅ Debug Mode: {Config.DEBUG}")
    
    return True

def test_database():
    """Test database initialization."""
    print("\n🗄️ Testing database...")
    
    try:
        from database import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_bot_creation():
    """Test bot creation."""
    print("\n🤖 Testing bot creation...")
    
    try:
        from bot.handlers import BotHandlers
        handlers = BotHandlers()
        print("✅ Bot handlers created successfully")
        return True
    except Exception as e:
        print(f"❌ Bot creation failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 PolyFocus Bot Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_configuration,
        test_database,
        test_bot_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        print("\n🚀 To start the bot, run: python start_bot.py")
        print("📱 Then find your bot at: t.me/Polymarketsolanabot")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Simple bot runner for production deployment
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

# Load configuration
load_env_file('bot_config.env')

# Set environment variables if not set
if not os.getenv('TELEGRAM_BOT_TOKEN'):
    print("❌ TELEGRAM_BOT_TOKEN not found")
    sys.exit(1)

if not os.getenv('ENCRYPTION_KEY'):
    print("❌ ENCRYPTION_KEY not found")
    sys.exit(1)

print("🚀 Starting PolyFocus Bot...")
print("=" * 40)

try:
    # Import and run the bot
    from bot.main import main
    main()
except KeyboardInterrupt:
    print("\n👋 Bot stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

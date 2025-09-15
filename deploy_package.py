#!/usr/bin/env python3
"""
Deployment Package Creator for PolyFocus Bot
This script prepares your bot for cloud deployment
"""

import os
import shutil
from pathlib import Path

def create_deployment_package():
    """Create a deployment-ready package."""
    print("📦 Creating Deployment Package...")
    print("=" * 40)
    
    # Create deployment directory
    deploy_dir = Path("deployment_package")
    deploy_dir.mkdir(exist_ok=True)
    
    # Files to include in deployment
    files_to_copy = [
        "simple_bot.py",
        "requirements.txt",
        "Procfile",
        "railway.json",
        "app.json",
        "README.md",
        "DEPLOYMENT_GUIDE.md",
        "GITHUB_SETUP.md"
    ]
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"✅ Copied {file}")
        else:
            print(f"⚠️  {file} not found")
    
    # Create environment template
    env_template = """# Environment Variables for Production
# Copy this to your hosting platform's environment variables

TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
POLYMARKET_API_KEY=your_polymarket_api_key_here
LIFI_API_KEY=your_lifi_api_key_here
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
DATABASE_URL=sqlite:///./data/polymarket_bot.db
HOST=0.0.0.0
PORT=8000
DEBUG=False
"""
    
    with open(deploy_dir / "env_template.txt", "w") as f:
        f.write(env_template)
    
    # Create simple requirements for deployment
    simple_requirements = """python-telegram-bot>=20.0
requests>=2.28.0
python-dotenv>=1.0.0
"""
    
    with open(deploy_dir / "requirements.txt", "w") as f:
        f.write(simple_requirements)
    
    # Create deployment instructions
    instructions = """# 🚀 PolyFocus Bot - Quick Deployment

## Your Bot Token
TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E

## Bot Link
https://t.me/Polymarketsolanabot

## Quick Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project
4. Connect your GitHub repository
5. Set environment variables:
   - TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
   - ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
6. Deploy!

## Quick Deploy to Heroku

1. Install Heroku CLI
2. heroku create your-bot-name
3. heroku config:set TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
4. heroku config:set ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
5. git push heroku main

## Test Your Bot
1. Go to https://t.me/Polymarketsolanabot
2. Send /start
3. Test all features!

Your bot will work perfectly from the cloud! 🎉
"""
    
    with open(deploy_dir / "QUICK_DEPLOY.md", "w") as f:
        f.write(instructions)
    
    print(f"\n✅ Deployment package created in: {deploy_dir}")
    print("\n📁 Files included:")
    for file in deploy_dir.iterdir():
        print(f"   • {file.name}")
    
    print("\n🚀 Next Steps:")
    print("1. Upload the deployment_package folder to GitHub")
    print("2. Deploy to Railway or Heroku")
    print("3. Test your bot: https://t.me/Polymarketsolanabot")
    
    return deploy_dir

if __name__ == '__main__':
    create_deployment_package()

# PolyFocus Bot - Quick Deployment Guide

## Your Bot Information
- **Bot Token**: 7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
- **Bot Link**: https://t.me/Polymarketsolanabot
- **Bot Username**: @Polymarketsolanabot

## Why Deploy to Cloud?
Since you're in Pakistan, Telegram API might be blocked locally. Deploying to a cloud server will solve this completely!

## Option 1: Railway (Recommended - Free)

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Create new project** → "Deploy from GitHub repo"
4. **Upload your code** to GitHub first
5. **Set environment variables**:
   - TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
   - ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
6. **Deploy** - Your bot will be live in minutes!

## Option 2: Heroku (Also Free)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-bot-name`
4. **Set environment variables**:
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
   heroku config:set ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
   ```
5. **Deploy**: `git push heroku main`

## Files You Need to Upload

Upload these files to GitHub:
- simple_bot.py (main bot file)
- requirements.txt
- Procfile
- railway.json
- app.json
- README.md

## Test Your Deployed Bot

1. **Go to**: https://t.me/Polymarketsolanabot
2. **Send**: /start
3. **Test features**: Use all menu buttons
4. **Search markets**: Send any text

## Environment Variables for Production

Set these in your hosting platform:

```
TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
POLYMARKET_API_KEY=your_polymarket_api_key_here
LIFI_API_KEY=your_lifi_api_key_here
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
DATABASE_URL=sqlite:///./data/polymarket_bot.db
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## Your Bot Features

- Trading on Polymarket
- Wallet management
- Referral system
- Copy trading
- Multi-language support
- Cross-chain bridge
- Real-time price tracking

## Success!

Once deployed, your bot will work 24/7 from the cloud server, bypassing any local connectivity issues in Pakistan!

**Bot Link**: https://t.me/Polymarketsolanabot
**Start Command**: /start

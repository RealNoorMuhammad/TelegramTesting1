# 🚀 PolyFocus Bot Deployment Guide

## 🌐 Deploy to Live Server (Recommended for Pakistan)

Since you're in Pakistan where Telegram might have connectivity issues, deploying to a cloud server is the best solution.

## 🎯 Quick Deployment Options

### Option 1: Railway (Easiest - Free Tier Available)

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Create new project** → "Deploy from GitHub repo"
4. **Connect your repository** (upload the code first)
5. **Set environment variables**:
   ```
   TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
   ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
   POLYMARKET_API_KEY=your_polymarket_api_key_here
   LIFI_API_KEY=your_lifi_api_key_here
   GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
   ```
6. **Deploy** - Railway will automatically build and run your bot

### Option 2: Heroku (Popular - Free Tier Available)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-bot-name`
4. **Set environment variables**:
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
   heroku config:set ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
   heroku config:set POLYMARKET_API_KEY=your_polymarket_api_key_here
   ```
5. **Deploy**: `git push heroku main`

### Option 3: DigitalOcean App Platform

1. **Go to**: https://cloud.digitalocean.com/apps
2. **Create app** → "Create from Source"
3. **Connect GitHub** and select your repository
4. **Configure**:
   - **Source**: Your repository
   - **Type**: Web Service
   - **Run Command**: `python run_bot.py`
   - **HTTP Port**: 8000
5. **Set environment variables** in the app settings
6. **Deploy**

### Option 4: VPS (Virtual Private Server)

#### Using DigitalOcean Droplet
1. **Create Droplet**: Ubuntu 22.04 LTS
2. **SSH into server**: `ssh root@your-server-ip`
3. **Install dependencies**:
   ```bash
   apt update
   apt install python3 python3-pip git
   ```
4. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/polymarket-bot.git
   cd polymarket-bot
   ```
5. **Install Python packages**:
   ```bash
   pip3 install -r requirements.txt
   ```
6. **Set environment variables**:
   ```bash
   export TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
   export ENCRYPTION_KEY=PolyFocus2024SecureKey32Char
   ```
7. **Run bot**:
   ```bash
   python3 run_bot.py
   ```

#### Using PM2 for Process Management
```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'polyfocus-bot',
    script: 'run_bot.py',
    interpreter: 'python3',
    env: {
      TELEGRAM_BOT_TOKEN: '7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E',
      ENCRYPTION_KEY: 'PolyFocus2024SecureKey32Char'
    }
  }]
}
EOF

# Start bot
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 🔧 Environment Variables for Production

Create a `.env` file or set these in your hosting platform:

```env
# Required
TELEGRAM_BOT_TOKEN=7822967965:AAGMau39Np0kF0brpKz_qYIdgBBzXeZzQ5E
ENCRYPTION_KEY=PolyFocus2024SecureKey32Char

# Optional APIs
POLYMARKET_API_KEY=your_polymarket_api_key_here
LIFI_API_KEY=your_lifi_api_key_here
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here

# Database (will be created automatically)
DATABASE_URL=sqlite:///./data/polymarket_bot.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## 📱 Testing Your Deployed Bot

1. **Find your bot**: https://t.me/Polymarketsolanabot
2. **Start the bot**: Send `/start`
3. **Test features**: Use all menu options
4. **Check logs**: Monitor your hosting platform's logs

## 🔍 Monitoring Your Bot

### Health Check Endpoint
Your bot includes a health check at `/health`:
```
https://your-app-url.railway.app/health
https://your-app-name.herokuapp.com/health
```

### Logs
- **Railway**: View logs in dashboard
- **Heroku**: `heroku logs --tail`
- **DigitalOcean**: View in app dashboard
- **VPS**: `pm2 logs polyfocus-bot`

## 🚨 Troubleshooting

### Bot Not Responding
1. Check if the process is running
2. Verify environment variables
3. Check logs for errors
4. Ensure internet connectivity

### Database Issues
1. Check if database file exists
2. Verify write permissions
3. Reset database if needed

### API Issues
1. Verify API keys are correct
2. Check API service status
3. Monitor rate limits

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Railway | ✅ 500 hours/month | $5/month | Easy deployment |
| Heroku | ✅ 550 hours/month | $7/month | Popular choice |
| DigitalOcean | ❌ | $5/month | Full control |
| VPS | ❌ | $3-10/month | Custom setup |

## 🎯 Recommended for Pakistan

**Best Option**: **Railway** or **Heroku**
- Free tier available
- Easy setup
- Reliable uptime
- Good for Pakistan connectivity

## 📞 Support

If you need help with deployment:
1. Check the logs first
2. Verify environment variables
3. Test locally first
4. Contact support

Your bot will work perfectly from any cloud server! 🚀

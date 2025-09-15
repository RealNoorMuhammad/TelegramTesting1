# GL Testing Bot 1.0.0 - Telegram Trading Bot

A comprehensive Telegram trading bot for Polymarket with advanced features including copy trading, referral system, multi-language support, and cross-chain bridging.

**Bot Username**: @GLtestingsolbot  
**Bot Link**: https://t.me/GLtestingsolbot

## 🚀 Features

### Core Trading Features
- **Polymarket Integration**: Full integration with Gamma, Data, and CLOB APIs
- **Order Management**: Place limit and market orders with slippage protection
- **Real-time Data**: Live price tracking and market updates via WebSocket
- **Portfolio Management**: Track positions, trades, and P&L

### Advanced Features
- **Copy Trading**: Follow successful traders with customizable risk parameters
- **Referral System**: Ponzi-style referral tree with permanent binding
- **Cross-chain Bridge**: LI.FI integration for POL ↔ other currencies
- **Multi-language Support**: 10+ languages with Google Translate API
- **Secure Wallet**: Encrypted private key storage

### User Interface
- **Intuitive Menu**: Clean Telegram interface with inline keyboards
- **Real-time Updates**: Live balances and price updates
- **Search Functionality**: Search markets by keywords
- **Settings Management**: Customizable slippage, gas fees, and language

## 📋 Prerequisites

- Python 3.11+
- Telegram Bot Token
- Polymarket API Key
- LI.FI API Key (optional)
- Google Translate API Key (optional)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd polymarket-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file with the following variables:

```env
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ENCRYPTION_KEY=your_32_character_encryption_key_here

# Polymarket APIs
POLYMARKET_GAMMA_API_URL=https://gamma-api.polymarket.com
POLYMARKET_DATA_API_URL=https://data-api.polymarket.com
POLYMARKET_CLOB_API_URL=https://clob.polymarket.com
POLYMARKET_API_KEY=your_polymarket_api_key_here

# Optional APIs
LIFI_API_URL=https://li.quest/v1
LIFI_API_KEY=your_lifi_api_key_here
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here

# Database
DATABASE_URL=sqlite:///./polymarket_bot.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 4. Initialize Database
```bash
python -c "from database import init_db; init_db()"
```

## 🚀 Running the Bot

### Development Mode
```bash
python main.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f polymarket-bot
```

### Production Deployment
```bash
# Build Docker image
docker build -t polymarket-bot .

# Run container
docker run -d \
  --name polymarket-bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -p 8000:8000 \
  polymarket-bot
```

## 📱 Bot Commands

### Main Commands
- `/start` - Initialize bot and show main menu
- Send any text to search for markets

### Menu Options
- **🎯 Your Positions** - View active positions and P&L
- **💳 Wallet** - Manage wallet, balances, and transfers
- **👥 Referral** - Referral system and rewards
- **📈 Copy Trading** - Follow and copy successful traders
- **👤 My Profile** - User profile and settings
- **⚙️ Settings** - Configure slippage, gas fees, language
- **❓ Help** - FAQ and support information
- **🔄 Refresh** - Update balances and prices

## 🔧 Configuration

### Trading Settings
- **Slippage Protection**: Default 10%, user configurable
- **Gas Fee Modes**: Fast (1.2x), Turbo (1.5x), Ultra (2.0x)
- **Order Types**: Limit orders and market orders

### Security Features
- **Encrypted Storage**: Private keys encrypted in database
- **Address Validation**: Ethereum address validation
- **Input Sanitization**: All user inputs validated

### Supported Languages
- English, Spanish, French, German, Italian
- Portuguese, Russian, Chinese, Japanese, Korean

## 📊 API Integration

### Polymarket APIs
- **Gamma API**: Events, markets, sports, search, orders
- **Data API**: Positions, trades, portfolio data
- **CLOB API**: Orderbook, prices, real-time updates

### External APIs
- **LI.FI Bridge**: Cross-chain token transfers
- **Google Translate**: Multi-language support
- **CoinGecko**: Token price data

## 🔒 Security

- Private keys encrypted with AES-256
- Database encryption for sensitive data
- Input validation and sanitization
- Secure API key management
- No private key exposure in logs

## 📈 Copy Trading

### Features
- Follow successful traders
- Automatic trade copying
- Risk management parameters
- Performance tracking
- Confidence thresholds

### Configuration
- Max position size per trade
- Max daily volume limit
- Copy percentage (0-100%)
- Minimum confidence threshold

## 👥 Referral System

### Features
- Unique referral codes
- Permanent binding to referrer
- 10% commission on referred user trades
- Ponzi-style visual display
- No retroactive changes allowed

### Rewards
- Commission on all referred user trades
- Multi-level referral tracking
- Automatic reward calculation
- Referral leaderboard

## 🌉 Cross-chain Bridge

### Supported Chains
- Polygon (POL)
- Ethereum (ETH)
- Solana (SOL) - Coming Soon

### Features
- LI.FI integration
- Real-time quotes
- Slippage protection
- Transaction tracking

## 📝 Database Schema

### Tables
- `users` - User accounts and settings
- `wallets` - Encrypted wallet information
- `positions` - Trading positions
- `trades` - Trade history
- `copy_trading_settings` - Copy trading configuration
- `referral_rewards` - Referral commission tracking
- `price_updates` - Token price history

## 🐛 Troubleshooting

### Common Issues
1. **Bot not responding**: Check TELEGRAM_BOT_TOKEN
2. **Database errors**: Ensure database permissions
3. **API errors**: Verify API keys and network connectivity
4. **Translation issues**: Check Google Translate API key

### Logs
```bash
# View application logs
tail -f polymarket_bot.log

# Docker logs
docker-compose logs -f polymarket-bot
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This bot is for educational and informational purposes only. Trading involves risk, and you should never trade with money you cannot afford to lose. The developers are not responsible for any financial losses.

## 📞 Support

- **Community**: [Telegram Channel](https://t.me/polyfocus_portal)
- **Documentation**: [docs.polyfocus.com](https://docs.polyfocus.com)
- **Support**: [Telegram Support](https://t.me/polyfocus_support)

## 🔄 Updates

### Version 1.0.0
- Initial release
- Core trading functionality
- Referral system
- Copy trading
- Multi-language support
- Cross-chain bridge integration

---

**GL Testing Bot 1.0.0** - Your gateway to decentralized prediction markets! 🚀

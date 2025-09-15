import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_URL')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./polymarket_bot.db')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    
    # Polymarket API Configuration
    POLYMARKET_GAMMA_API_URL = os.getenv('POLYMARKET_GAMMA_API_URL', 'https://gamma-api.polymarket.com')
    POLYMARKET_DATA_API_URL = os.getenv('POLYMARKET_DATA_API_URL', 'https://data-api.polymarket.com')
    POLYMARKET_CLOB_API_URL = os.getenv('POLYMARKET_CLOB_API_URL', 'https://clob.polymarket.com')
    POLYMARKET_API_KEY = os.getenv('POLYMARKET_API_KEY')
    
    # LI.FI Bridge API
    LIFI_API_URL = os.getenv('LIFI_API_URL', 'https://li.quest/v1')
    LIFI_API_KEY = os.getenv('LIFI_API_KEY')
    
    # Google Translate API
    GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY')
    
    # WebSocket Configuration
    WEBSOCKET_URL = os.getenv('WEBSOCKET_URL', 'wss://clob.polymarket.com/ws')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Trading Configuration
    DEFAULT_SLIPPAGE = 0.10  # 10%
    GAS_FEE_MODES = {
        'fast': 1.2,
        'turbo': 1.5,
        'ultra': 2.0
    }
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean'
    }

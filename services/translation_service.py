from typing import Dict, Optional
from config import Config
import asyncio
import requests

class TranslationService:
    """Service for multi-language support using Google Translate API."""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_TRANSLATE_API_KEY
        self.supported_languages = Config.SUPPORTED_LANGUAGES
    
    async def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """Translate text to target language."""
        try:
            if not self.api_key or self.api_key == 'your_google_translate_api_key_here':
                return text  # Return original text if no API key
            
            # Use Google Translate API via HTTP
            url = f"https://translation.googleapis.com/language/translate/v2?key={self.api_key}"
            data = {
                'q': text,
                'target': target_language,
                'source': source_language
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['translations'][0]['translatedText']
            else:
                return text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    async def translate_message(self, message: str, target_language: str) -> str:
        """Translate a complete message with proper formatting."""
        # Split message into parts to preserve formatting
        lines = message.split('\n')
        translated_lines = []
        
        for line in lines:
            if line.strip() and not line.startswith('`') and not line.startswith('*'):
                # Translate only non-code and non-markdown lines
                translated_line = await self.translate_text(line, target_language)
                translated_lines.append(translated_line)
            else:
                translated_lines.append(line)
        
        return '\n'.join(translated_lines)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages."""
        return self.supported_languages
    
    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported."""
        return language_code in self.supported_languages
    
    async def translate_ui_text(self, text_key: str, language: str) -> str:
        """Translate UI text based on key and language."""
        # UI text translations
        ui_texts = {
            'welcome_title': {
                'en': '🚀 **PolyFocus 1.0.0**',
                'es': '🚀 **PolyFocus 1.0.0**',
                'fr': '🚀 **PolyFocus 1.0.0**',
                'de': '🚀 **PolyFocus 1.0.0**',
                'it': '🚀 **PolyFocus 1.0.0**',
                'pt': '🚀 **PolyFocus 1.0.0**',
                'ru': '🚀 **PolyFocus 1.0.0**',
                'zh': '🚀 **PolyFocus 1.0.0**',
                'ja': '🚀 **PolyFocus 1.0.0**',
                'ko': '🚀 **PolyFocus 1.0.0**'
            },
            'user_info': {
                'en': '👤 **User Info:**',
                'es': '👤 **Información del Usuario:**',
                'fr': '👤 **Informations Utilisateur:**',
                'de': '👤 **Benutzerinformationen:**',
                'it': '👤 **Informazioni Utente:**',
                'pt': '👤 **Informações do Usuário:**',
                'ru': '👤 **Информация о Пользователе:**',
                'zh': '👤 **用户信息:**',
                'ja': '👤 **ユーザー情報:**',
                'ko': '👤 **사용자 정보:**'
            },
            'live_balances': {
                'en': '💰 **Live Balances:**',
                'es': '💰 **Saldos en Vivo:**',
                'fr': '💰 **Soldes en Direct:**',
                'de': '💰 **Live-Salden:**',
                'it': '💰 **Saldo in Tempo Reale:**',
                'pt': '💰 **Saldos ao Vivo:**',
                'ru': '💰 **Живые Балансы:**',
                'zh': '💰 **实时余额:**',
                'ja': '💰 **ライブ残高:**',
                'ko': '💰 **실시간 잔액:**'
            },
            'positions': {
                'en': '🎯 Your Positions',
                'es': '🎯 Tus Posiciones',
                'fr': '🎯 Vos Positions',
                'de': '🎯 Ihre Positionen',
                'it': '🎯 Le Tue Posizioni',
                'pt': '🎯 Suas Posições',
                'ru': '🎯 Ваши Позиции',
                'zh': '🎯 您的持仓',
                'ja': '🎯 あなたのポジション',
                'ko': '🎯 귀하의 포지션'
            },
            'wallet': {
                'en': '💳 Wallet',
                'es': '💳 Cartera',
                'fr': '💳 Portefeuille',
                'de': '💳 Wallet',
                'it': '💳 Portafoglio',
                'pt': '💳 Carteira',
                'ru': '💳 Кошелек',
                'zh': '💳 钱包',
                'ja': '💳 ウォレット',
                'ko': '💳 지갑'
            },
            'referral': {
                'en': '👥 Referral',
                'es': '👥 Referido',
                'fr': '👥 Parrainage',
                'de': '👥 Empfehlung',
                'it': '👥 Referral',
                'pt': '👥 Indicação',
                'ru': '👥 Реферал',
                'zh': '👥 推荐',
                'ja': '👥 紹介',
                'ko': '👥 추천'
            },
            'copy_trading': {
                'en': '📈 Copy Trading',
                'es': '📈 Trading de Copia',
                'fr': '📈 Trading de Copie',
                'de': '📈 Copy Trading',
                'it': '📈 Copy Trading',
                'pt': '📈 Copy Trading',
                'ru': '📈 Копирование Торговли',
                'zh': '📈 跟单交易',
                'ja': '📈 コピートレーディング',
                'ko': '📈 복사 거래'
            },
            'settings': {
                'en': '⚙️ Settings',
                'es': '⚙️ Configuración',
                'fr': '⚙️ Paramètres',
                'de': '⚙️ Einstellungen',
                'it': '⚙️ Impostazioni',
                'pt': '⚙️ Configurações',
                'ru': '⚙️ Настройки',
                'zh': '⚙️ 设置',
                'ja': '⚙️ 設定',
                'ko': '⚙️ 설정'
            },
            'help': {
                'en': '❓ Help',
                'es': '❓ Ayuda',
                'fr': '❓ Aide',
                'de': '❓ Hilfe',
                'it': '❓ Aiuto',
                'pt': '❓ Ajuda',
                'ru': '❓ Помощь',
                'zh': '❓ 帮助',
                'ja': '❓ ヘルプ',
                'ko': '❓ 도움말'
            }
        }
        
        if text_key in ui_texts and language in ui_texts[text_key]:
            return ui_texts[text_key][language]
        else:
            # Fallback to English
            return ui_texts[text_key].get('en', text_key)
    
    async def translate_error_message(self, error: str, language: str) -> str:
        """Translate error messages."""
        error_translations = {
            'user_not_found': {
                'en': 'User not found. Please use /start first.',
                'es': 'Usuario no encontrado. Por favor usa /start primero.',
                'fr': 'Utilisateur non trouvé. Veuillez utiliser /start d\'abord.',
                'de': 'Benutzer nicht gefunden. Bitte verwenden Sie zuerst /start.',
                'it': 'Utente non trovato. Si prega di utilizzare /start prima.',
                'pt': 'Usuário não encontrado. Por favor use /start primeiro.',
                'ru': 'Пользователь не найден. Пожалуйста, сначала используйте /start.',
                'zh': '未找到用户。请先使用 /start。',
                'ja': 'ユーザーが見つかりません。まず /start を使用してください。',
                'ko': '사용자를 찾을 수 없습니다. 먼저 /start를 사용하세요.'
            },
            'wallet_not_connected': {
                'en': 'No wallet connected. Connect a wallet to start trading!',
                'es': 'No hay cartera conectada. ¡Conecta una cartera para comenzar a operar!',
                'fr': 'Aucun portefeuille connecté. Connectez un portefeuille pour commencer à trader !',
                'de': 'Keine Wallet verbunden. Verbinden Sie eine Wallet, um mit dem Trading zu beginnen!',
                'it': 'Nessun portafoglio connesso. Collega un portafoglio per iniziare a fare trading!',
                'pt': 'Nenhuma carteira conectada. Conecte uma carteira para começar a negociar!',
                'ru': 'Кошелек не подключен. Подключите кошелек, чтобы начать торговать!',
                'zh': '未连接钱包。连接钱包开始交易！',
                'ja': 'ウォレットが接続されていません。取引を開始するためにウォレットを接続してください！',
                'ko': '지갑이 연결되지 않았습니다. 거래를 시작하려면 지갑을 연결하세요!'
            }
        }
        
        if error in error_translations and language in error_translations[error]:
            return error_translations[error][language]
        else:
            return error_translations[error].get('en', error)

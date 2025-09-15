import secrets
import string
from typing import Dict, Any
from datetime import datetime

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency amount with proper symbols and decimals."""
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'POL':
        return f"{amount:,.2f} POL"
    elif currency == 'USDC':
        return f"{amount:,.2f} USDC"
    elif currency == 'ETH':
        return f"{amount:.4f} ETH"
    else:
        return f"{amount:,.2f} {currency}"

def format_percentage(value: float) -> str:
    """Format percentage value."""
    return f"{value * 100:.1f}%"

def format_number(value: float, decimals: int = 2) -> str:
    """Format number with specified decimal places."""
    return f"{value:,.{decimals}f}"

def generate_referral_code(length: int = 8) -> str:
    """Generate a random referral code."""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display."""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')

def format_relative_time(timestamp: datetime) -> str:
    """Format relative time (e.g., '2 hours ago')."""
    now = datetime.utcnow()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_market_title(title: str, max_length: int = 50) -> str:
    """Format market title for display."""
    return truncate_text(title, max_length)

def calculate_pnl(entry_price: float, current_price: float, shares: float, side: str) -> float:
    """Calculate profit/loss for a position."""
    if side.upper() == 'BUY':
        return (current_price - entry_price) * shares
    else:  # SELL
        return (entry_price - current_price) * shares

def calculate_roi(entry_price: float, current_price: float, side: str) -> float:
    """Calculate return on investment percentage."""
    if side.upper() == 'BUY':
        return (current_price - entry_price) / entry_price
    else:  # SELL
        return (entry_price - current_price) / entry_price

def format_pnl(pnl: float) -> str:
    """Format P&L with appropriate emoji and color."""
    if pnl > 0:
        return f"📈 +{format_currency(pnl)}"
    elif pnl < 0:
        return f"📉 {format_currency(pnl)}"
    else:
        return f"➡️ {format_currency(pnl)}"

def validate_wallet_address(address: str) -> bool:
    """Validate Ethereum wallet address."""
    if not address or not isinstance(address, str):
        return False
    
    # Basic Ethereum address validation
    if not address.startswith('0x'):
        return False
    
    if len(address) != 42:
        return False
    
    try:
        int(address[2:], 16)
        return True
    except ValueError:
        return False

def validate_amount(amount: str) -> tuple[bool, float]:
    """Validate and parse amount string."""
    try:
        value = float(amount)
        if value <= 0:
            return False, 0.0
        return True, value
    except ValueError:
        return False, 0.0

def validate_price(price: str) -> tuple[bool, float]:
    """Validate and parse price string."""
    try:
        value = float(price)
        if value < 0 or value > 1:
            return False, 0.0
        return True, value
    except ValueError:
        return False, 0.0

def format_order_status(status: str) -> str:
    """Format order status with emoji."""
    status_emojis = {
        'pending': '⏳ Pending',
        'filled': '✅ Filled',
        'cancelled': '❌ Cancelled',
        'failed': '💥 Failed',
        'partially_filled': '🔄 Partially Filled'
    }
    return status_emojis.get(status.lower(), status)

def format_trade_side(side: str) -> str:
    """Format trade side with emoji."""
    if side.upper() == 'BUY':
        return '🟢 BUY'
    elif side.upper() == 'SELL':
        return '🔴 SELL'
    else:
        return side

def format_outcome(outcome: str) -> str:
    """Format market outcome with emoji."""
    if outcome.upper() == 'YES':
        return '✅ YES'
    elif outcome.upper() == 'NO':
        return '❌ NO'
    else:
        return outcome

def create_progress_bar(current: float, total: float, length: int = 20) -> str:
    """Create a text-based progress bar."""
    if total == 0:
        return "█" * length
    
    filled = int((current / total) * length)
    bar = "█" * filled + "░" * (length - filled)
    percentage = (current / total) * 100
    
    return f"{bar} {percentage:.1f}%"

def format_large_number(number: float) -> str:
    """Format large numbers with K, M, B suffixes."""
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return f"{number:.2f}"

def get_risk_level(volatility: float) -> str:
    """Get risk level based on volatility."""
    if volatility < 0.1:
        return "🟢 Low Risk"
    elif volatility < 0.3:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

def format_confidence(confidence: float) -> str:
    """Format confidence percentage."""
    if confidence >= 0.8:
        return f"🟢 {confidence * 100:.0f}%"
    elif confidence >= 0.6:
        return f"🟡 {confidence * 100:.0f}%"
    else:
        return f"🔴 {confidence * 100:.0f}%"

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from database import get_db, User, Wallet, Position, Trade, CopyTradingSettings
from apis import PolymarketGammaAPI, PolymarketDataAPI, PolymarketCLOBAPI, LifiBridgeAPI, PriceTracker
from services.wallet_service import WalletService
from services.trading_service import TradingService
from services.referral_service import ReferralService
from services.translation_service import TranslationService
from utils.helpers import format_currency, format_percentage, generate_referral_code

class BotHandlers:
    def __init__(self):
        self.gamma_api = PolymarketGammaAPI()
        self.data_api = PolymarketDataAPI()
        self.clob_api = PolymarketCLOBAPI()
        self.lifi_api = LifiBridgeAPI()
        self.price_tracker = PriceTracker()
        self.wallet_service = WalletService()
        self.trading_service = TradingService()
        self.referral_service = ReferralService()
        self.translation_service = TranslationService()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - show branding and main menu."""
        user = update.effective_user
        user_id = user.id
        
        # Get or create user in database
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            # Create new user
            db_user = User(
                telegram_id=user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                referral_code=generate_referral_code()
            )
            db.add(db_user)
            db.commit()
        
        # Get user's wallet and balances
        wallet = db.query(Wallet).filter(Wallet.user_id == db_user.id, Wallet.is_active == True).first()
        
        # Get live prices
        prices = await self.price_tracker.get_multiple_prices(['POL', 'USDC'])
        
        # Calculate portfolio value
        positions = db.query(Position).filter(Position.user_id == db_user.id).all()
        portfolio_value = await self.price_tracker.get_portfolio_value(positions, prices)
        
        # Format balances
        pol_balance = 0.0
        usdc_balance = 0.0
        if wallet:
            # In a real implementation, you'd fetch actual balances from the blockchain
            pol_balance = 1000.0  # Mock data
            usdc_balance = 500.0  # Mock data
        
        # Create welcome message
        welcome_text = f"""
🚀 **PolyFocus 1.0.0**

👤 **User Info:**
• Username: @{user.username or 'N/A'}
• Wallet: `{wallet.address if wallet else 'Not connected'}`

💰 **Live Balances:**
• POL: {format_currency(pol_balance)} (${format_currency(pol_balance * prices.get('POL', {}).get('price_usd', 0))})
• USDC.e: {format_currency(usdc_balance)}
• SOL: Coming Soon
• **Total Portfolio:** ${format_currency(portfolio_value)}

🕐 Last Update: {datetime.now().strftime('%H:%M:%S UTC')}

🔍 **Search Markets:** Send any text to search for prediction markets (e.g., "trump", "election", "bitcoin")
"""
        
        # Create main menu keyboard
        keyboard = [
            [InlineKeyboardButton("🎯 Your Positions", callback_data="positions")],
            [InlineKeyboardButton("💳 Wallet", callback_data="wallet")],
            [InlineKeyboardButton("👥 Referral", callback_data="referral")],
            [InlineKeyboardButton("📡 Community", url="https://t.me/polyfocus_portal")],
            [InlineKeyboardButton("📈 Copy Trading", callback_data="copy_trading")],
            [InlineKeyboardButton("👤 My Profile", callback_data="profile")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
            [InlineKeyboardButton("❓ Help", callback_data="help")],
            [InlineKeyboardButton("📒 Docs", url="https://docs.polyfocus.com")],
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline keyboards."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        if data == "positions":
            await self.show_positions(query)
        elif data == "wallet":
            await self.show_wallet(query)
        elif data == "referral":
            await self.show_referral(query)
        elif data == "copy_trading":
            await self.show_copy_trading(query)
        elif data == "profile":
            await self.show_profile(query)
        elif data == "settings":
            await self.show_settings(query)
        elif data == "help":
            await self.show_help(query)
        elif data == "refresh":
            await self.refresh_data(query)
        elif data.startswith("back_to_main"):
            await self.start_command(update, context)
    
    async def show_positions(self, query):
        """Show user's positions dashboard."""
        user_id = query.from_user.id
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            await query.edit_message_text("User not found. Please use /start first.")
            return
        
        positions = db.query(Position).filter(Position.user_id == db_user.id).all()
        
        if not positions:
            text = "📊 **Your Positions**\n\nNo positions found. Start trading to see your positions here!"
        else:
            text = "📊 **Your Positions**\n\n"
            total_pnl = 0
            
            for pos in positions:
                pnl_emoji = "📈" if pos.unrealized_pnl > 0 else "📉" if pos.unrealized_pnl < 0 else "➡️"
                text += f"{pnl_emoji} **{pos.market_title}**\n"
                text += f"• Outcome: {pos.outcome}\n"
                text += f"• Shares: {pos.shares:.2f}\n"
                text += f"• Avg Price: ${pos.average_price:.3f}\n"
                text += f"• Current: ${pos.current_price:.3f}\n"
                text += f"• P&L: {format_currency(pos.unrealized_pnl)}\n\n"
                total_pnl += pos.unrealized_pnl
            
            text += f"**Total P&L:** {format_currency(total_pnl)}"
        
        keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def show_wallet(self, query):
        """Show wallet management interface."""
        user_id = query.from_user.id
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            await query.edit_message_text("User not found. Please use /start first.")
            return
        
        wallet = db.query(Wallet).filter(Wallet.user_id == db_user.id, Wallet.is_active == True).first()
        
        if not wallet:
            text = "💳 **Wallet Management**\n\nNo wallet connected. Connect a wallet to start trading!"
            keyboard = [
                [InlineKeyboardButton("🔗 Connect Wallet", callback_data="connect_wallet")],
                [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
            ]
        else:
            # Get balances (mock data for now)
            pol_balance = 1000.0
            usdc_balance = 500.0
            
            text = f"💳 **Wallet Management**\n\n"
            text += f"**Address:** `{wallet.address}`\n"
            text += f"**Network:** {wallet.network.upper()}\n\n"
            text += f"**Balances:**\n"
            text += f"• POL: {format_currency(pol_balance)}\n"
            text += f"• USDC.e: {format_currency(usdc_balance)}\n\n"
            text += f"**Actions:**"
            
            keyboard = [
                [InlineKeyboardButton("💸 Send", callback_data="send_tokens")],
                [InlineKeyboardButton("🌉 Bridge", callback_data="bridge_tokens")],
                [InlineKeyboardButton("📊 Portfolio", callback_data="portfolio")],
                [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def show_referral(self, query):
        """Show referral system interface."""
        user_id = query.from_user.id
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            await query.edit_message_text("User not found. Please use /start first.")
            return
        
        # Get referral stats
        referrals = db.query(User).filter(User.referrer_id == db_user.id).count()
        total_rewards = 0.0  # Calculate from ReferralReward table
        
        text = f"👥 **Referral System**\n\n"
        text += f"**Your Referral Code:** `{db_user.referral_code}`\n\n"
        text += f"**Stats:**\n"
        text += f"• Total Referrals: {referrals}\n"
        text += f"• Total Rewards: ${format_currency(total_rewards)}\n\n"
        text += f"**Share your link:**\n"
        text += f"`https://t.me/your_bot?start={db_user.referral_code}`\n\n"
        text += f"**Referral Tree:**\n"
        text += f"🔗 You are at the top of the pyramid!\n"
        text += f"📊 Earn 10% commission from all your referrals' trades!"
        
        keyboard = [
            [InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_referral_{db_user.referral_code}")],
            [InlineKeyboardButton("📊 View Tree", callback_data="referral_tree")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def show_copy_trading(self, query):
        """Show copy trading interface."""
        user_id = query.from_user.id
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            await query.edit_message_text("User not found. Please use /start first.")
            return
        
        copy_settings = db.query(CopyTradingSettings).filter(CopyTradingSettings.user_id == db_user.id).first()
        
        if not copy_settings:
            # Create default settings
            copy_settings = CopyTradingSettings(
                user_id=db_user.id,
                is_enabled=False,
                max_position_size=1000.0,
                max_daily_volume=10000.0,
                copy_percentage=1.0,
                min_confidence=0.7
            )
            db.add(copy_settings)
            db.commit()
        
        status_emoji = "✅" if copy_settings.is_enabled else "❌"
        
        text = f"📈 **Copy Trading**\n\n"
        text += f"**Status:** {status_emoji} {'Enabled' if copy_settings.is_enabled else 'Disabled'}\n\n"
        text += f"**Settings:**\n"
        text += f"• Max Position Size: ${format_currency(copy_settings.max_position_size)}\n"
        text += f"• Max Daily Volume: ${format_currency(copy_settings.max_daily_volume)}\n"
        text += f"• Copy Percentage: {format_percentage(copy_settings.copy_percentage)}\n"
        text += f"• Min Confidence: {format_percentage(copy_settings.min_confidence)}\n\n"
        text += f"**How it works:**\n"
        text += f"1. Follow successful traders\n"
        text += f"2. Automatically copy their trades\n"
        text += f"3. Set your risk parameters\n"
        text += f"4. Earn while you sleep!"
        
        keyboard = [
            [InlineKeyboardButton("⚙️ Configure", callback_data="configure_copy_trading")],
            [InlineKeyboardButton("👥 Follow Traders", callback_data="follow_traders")],
            [InlineKeyboardButton("📊 Performance", callback_data="copy_performance")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def show_profile(self, query):
        """Show user profile."""
        user_id = query.from_user.id
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            await query.edit_message_text("User not found. Please use /start first.")
            return
        
        # Get user stats
        total_trades = db.query(Trade).filter(Trade.user_id == db_user.id).count()
        total_positions = db.query(Position).filter(Position.user_id == db_user.id).count()
        referrals = db.query(User).filter(User.referrer_id == db_user.id).count()
        
        text = f"👤 **My Profile**\n\n"
        text += f"**User Info:**\n"
        text += f"• Username: @{db_user.username or 'N/A'}\n"
        text += f"• Name: {db_user.first_name} {db_user.last_name or ''}\n"
        text += f"• Language: {db_user.language.upper()}\n"
        text += f"• Member Since: {db_user.created_at.strftime('%Y-%m-%d')}\n\n"
        text += f"**Trading Stats:**\n"
        text += f"• Total Trades: {total_trades}\n"
        text += f"• Active Positions: {total_positions}\n"
        text += f"• Referrals: {referrals}\n\n"
        text += f"**Settings:**\n"
        text += f"• Slippage: {format_percentage(db_user.slippage_tolerance)}\n"
        text += f"• Gas Mode: {db_user.gas_fee_mode.title()}\n"
        text += f"• Last Active: {db_user.last_active.strftime('%Y-%m-%d %H:%M')}"
        
        keyboard = [
            [InlineKeyboardButton("⚙️ Edit Profile", callback_data="edit_profile")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def show_settings(self, query):
        """Show settings interface."""
        user_id = query.from_user.id
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not db_user:
            await query.edit_message_text("User not found. Please use /start first.")
            return
        
        text = f"⚙️ **Settings**\n\n"
        text += f"**Trading Settings:**\n"
        text += f"• Slippage Tolerance: {format_percentage(db_user.slippage_tolerance)}\n"
        text += f"• Gas Fee Mode: {db_user.gas_fee_mode.title()}\n\n"
        text += f"**Language Settings:**\n"
        text += f"• Current Language: {db_user.language.upper()}\n\n"
        text += f"**Security Settings:**\n"
        text += f"• Private Key: Encrypted ✅\n"
        text += f"• 2FA: Not enabled\n\n"
        text += f"**Gas Fee Modes:**\n"
        text += f"• Fast: 1.2x base fee\n"
        text += f"• Turbo: 1.5x base fee\n"
        text += f"• Ultra: 2.0x base fee"
        
        keyboard = [
            [InlineKeyboardButton("🎯 Slippage", callback_data="set_slippage")],
            [InlineKeyboardButton("⛽ Gas Fees", callback_data="set_gas_fees")],
            [InlineKeyboardButton("🌐 Language", callback_data="set_language")],
            [InlineKeyboardButton("🔒 Security", callback_data="security_settings")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def show_help(self, query):
        """Show help and FAQ."""
        text = f"❓ **Help & FAQ**\n\n"
        text += f"**Getting Started:**\n"
        text += f"1. Connect your wallet\n"
        text += f"2. Search for markets\n"
        text += f"3. Place your first trade\n"
        text += f"4. Monitor your positions\n\n"
        text += f"**Trading:**\n"
        text += f"• Send any text to search markets\n"
        text += f"• Use limit orders for better prices\n"
        text += f"• Set slippage protection\n"
        text += f"• Monitor gas fees\n\n"
        text += f"• **Copy Trading:** Follow successful traders\n"
        text += f"• **Referrals:** Share your link to earn\n"
        text += f"• **Bridge:** Transfer tokens between chains\n\n"
        text += f"**Need More Help?**\n"
        text += f"• Join our community: @polyfocus_portal\n"
        text += f"• Read docs: docs.polyfocus.com\n"
        text += f"• Contact support: @polyfocus_support"
        
        keyboard = [
            [InlineKeyboardButton("📒 Documentation", url="https://docs.polyfocus.com")],
            [InlineKeyboardButton("📡 Community", url="https://t.me/polyfocus_portal")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def refresh_data(self, query):
        """Refresh user data and prices."""
        user_id = query.from_user.id
        
        # Update prices
        prices = await self.price_tracker.get_multiple_prices(['POL', 'USDC'])
        
        # Update user's last active time
        db = next(get_db())
        db_user = db.query(User).filter(User.telegram_id == user_id).first()
        if db_user:
            db_user.last_active = datetime.utcnow()
            db.commit()
        
        await query.answer("✅ Data refreshed successfully!")
        
        # Go back to main menu
        await self.start_command(query, None)
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages as market search queries."""
        query_text = update.message.text
        user_id = update.effective_user.id
        
        # Search for markets
        try:
            markets = await self.gamma_api.search_markets(query_text, limit=10)
            
            if not markets:
                await update.message.reply_text(f"🔍 No markets found for '{query_text}'. Try a different search term.")
                return
            
            text = f"🔍 **Search Results for '{query_text}'**\n\n"
            
            keyboard = []
            for i, market in enumerate(markets[:5]):  # Show top 5 results
                market_id = market.get('id', '')
                market_title = market.get('title', 'Unknown Market')
                market_description = market.get('description', '')[:100] + '...' if len(market.get('description', '')) > 100 else market.get('description', '')
                
                text += f"**{i+1}. {market_title}**\n"
                text += f"{market_description}\n\n"
                
                keyboard.append([InlineKeyboardButton(f"📊 View Market {i+1}", callback_data=f"view_market_{market_id}")])
            
            keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error searching markets: {str(e)}")

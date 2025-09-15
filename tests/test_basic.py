"""
Basic tests for PolyFocus Bot
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from database import init_db, User, Wallet
from services.wallet_service import WalletService
from services.trading_service import TradingService
from services.referral_service import ReferralService
from utils.helpers import format_currency, validate_wallet_address, generate_referral_code

class TestWalletService:
    """Test wallet service functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        init_db()
        self.wallet_service = WalletService()
    
    def test_generate_wallet(self):
        """Test wallet generation."""
        wallet_data = self.wallet_service.generate_wallet()
        
        assert 'address' in wallet_data
        assert 'private_key' in wallet_data
        assert wallet_data['address'].startswith('0x')
        assert len(wallet_data['address']) == 42
        assert len(wallet_data['private_key']) == 64
    
    def test_validate_wallet_address(self):
        """Test wallet address validation."""
        # Valid addresses
        assert validate_wallet_address('0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6')
        assert validate_wallet_address('0x0000000000000000000000000000000000000000')
        
        # Invalid addresses
        assert not validate_wallet_address('invalid_address')
        assert not validate_wallet_address('0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b')
        assert not validate_wallet_address('742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6')
        assert not validate_wallet_address('')

class TestTradingService:
    """Test trading service functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        init_db()
        self.trading_service = TradingService()
    
    @pytest.mark.asyncio
    async def test_place_limit_order_mock(self):
        """Test placing a limit order with mocked API."""
        with patch('apis.polymarket_gamma.PolymarketGammaAPI.place_limit_order') as mock_place:
            mock_place.return_value = {'order_id': 'test_order_123'}
            
            result = await self.trading_service.place_limit_order(
                user_id=1,
                market_id='test_market',
                outcome='YES',
                side='BUY',
                shares=10.0,
                price=0.6
            )
            
            assert result['success'] is True
            assert 'order_id' in result
            assert 'trade_id' in result

class TestReferralService:
    """Test referral service functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        init_db()
        self.referral_service = ReferralService()
    
    def test_generate_referral_code(self):
        """Test referral code generation."""
        code1 = self.referral_service.generate_referral_code()
        code2 = self.referral_service.generate_referral_code()
        
        assert len(code1) == 8
        assert len(code2) == 8
        assert code1 != code2  # Should be unique
    
    def test_calculate_referral_reward(self):
        """Test referral reward calculation."""
        reward = self.referral_service.calculate_referral_reward(1000.0, 0.10)
        assert reward == 100.0
        
        reward = self.referral_service.calculate_referral_reward(500.0, 0.05)
        assert reward == 25.0

class TestHelpers:
    """Test utility helper functions."""
    
    def test_format_currency(self):
        """Test currency formatting."""
        assert format_currency(1234.56) == "$1,234.56"
        assert format_currency(1000.0, 'POL') == "1,000.00 POL"
        assert format_currency(0.5, 'ETH') == "0.5000 ETH"
    
    def test_generate_referral_code(self):
        """Test referral code generation."""
        code = generate_referral_code()
        assert len(code) == 8
        assert code.isalnum()
        assert code.isupper()

class TestDatabase:
    """Test database functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        init_db()
    
    def test_user_creation(self):
        """Test user creation in database."""
        db = next(get_db())
        
        user = User(
            telegram_id=12345,
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        
        db.add(user)
        db.commit()
        
        # Verify user was created
        created_user = db.query(User).filter(User.telegram_id == 12345).first()
        assert created_user is not None
        assert created_user.username == 'testuser'
        assert created_user.first_name == 'Test'

if __name__ == '__main__':
    pytest.main([__file__])

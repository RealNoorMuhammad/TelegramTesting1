from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    language = Column(String(10), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Referral system
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    referral_code = Column(String(50), unique=True)
    
    # Settings
    slippage_tolerance = Column(Float, default=0.10)  # 10%
    gas_fee_mode = Column(String(20), default='fast')
    
    # Relationships
    referrer = relationship("User", remote_side=[id], backref="referrals")
    wallets = relationship("Wallet", back_populates="user")
    positions = relationship("Position", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    copy_trading_settings = relationship("CopyTradingSettings", back_populates="user")

class Wallet(Base):
    __tablename__ = 'wallets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address = Column(String(255), nullable=False)
    encrypted_private_key = Column(Text, nullable=False)  # Encrypted private key
    network = Column(String(50), default='polygon')  # polygon, ethereum, solana
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wallets")

class Position(Base):
    __tablename__ = 'positions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    market_id = Column(String(255), nullable=False)
    market_title = Column(String(500))
    outcome = Column(String(100))  # YES, NO, or specific outcome
    shares = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    current_price = Column(Float)
    unrealized_pnl = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="positions")

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    market_id = Column(String(255), nullable=False)
    outcome = Column(String(100))
    side = Column(String(10), nullable=False)  # BUY, SELL
    order_type = Column(String(20), nullable=False)  # LIMIT, MARKET
    shares = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    fees = Column(Float, default=0.0)
    status = Column(String(20), default='pending')  # pending, filled, cancelled, failed
    order_id = Column(String(255))
    transaction_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    filled_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="trades")

class CopyTradingSettings(Base):
    __tablename__ = 'copy_trading_settings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_enabled = Column(Boolean, default=False)
    max_position_size = Column(Float, default=1000.0)  # Max USD per position
    max_daily_volume = Column(Float, default=10000.0)  # Max USD per day
    copy_percentage = Column(Float, default=1.0)  # 100% of copied trades
    min_confidence = Column(Float, default=0.7)  # Min confidence threshold
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="copy_trading_settings")

class ReferralReward(Base):
    __tablename__ = 'referral_rewards'
    
    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    referred_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reward_amount = Column(Float, default=0.0)
    reward_type = Column(String(50), default='commission')  # commission, bonus, etc.
    status = Column(String(20), default='pending')  # pending, paid, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    
    # Relationships
    referrer = relationship("User", foreign_keys=[referrer_id])
    referred = relationship("User", foreign_keys=[referred_id])

class PriceUpdate(Base):
    __tablename__ = 'price_updates'
    
    id = Column(Integer, primary_key=True)
    token_symbol = Column(String(20), nullable=False)
    price_usd = Column(Float, nullable=False)
    price_change_24h = Column(Float, default=0.0)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)

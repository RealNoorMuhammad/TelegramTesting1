from typing import Dict, List, Optional, Any
from database import get_db, User, Trade, Position
from apis import PolymarketGammaAPI, PolymarketDataAPI, PolymarketCLOBAPI
from services.wallet_service import WalletService
import asyncio
from datetime import datetime

class TradingService:
    """Service for trading operations and order management."""
    
    def __init__(self):
        self.gamma_api = PolymarketGammaAPI()
        self.data_api = PolymarketDataAPI()
        self.clob_api = PolymarketCLOBAPI()
        self.wallet_service = WalletService()
    
    async def place_limit_order(self, user_id: int, market_id: str, outcome: str, 
                              side: str, shares: float, price: float, 
                              slippage_tolerance: float = 0.10) -> Dict:
        """Place a limit order."""
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        wallet = self.wallet_service.get_user_wallet(user_id)
        
        if not user or not wallet:
            return {'success': False, 'error': 'User or wallet not found'}
        
        try:
            # Prepare order data
            order_data = {
                'market_id': market_id,
                'outcome': outcome,
                'side': side.upper(),  # BUY or SELL
                'shares': shares,
                'price': price,
                'slippage_tolerance': slippage_tolerance,
                'wallet_address': wallet.address
            }
            
            # Place order via Gamma API
            result = await self.gamma_api.place_limit_order(order_data)
            
            # Create trade record
            trade = Trade(
                user_id=user_id,
                market_id=market_id,
                outcome=outcome,
                side=side.upper(),
                order_type='LIMIT',
                shares=shares,
                price=price,
                total_amount=shares * price,
                status='pending',
                order_id=result.get('order_id')
            )
            
            db.add(trade)
            db.commit()
            
            return {
                'success': True,
                'order_id': result.get('order_id'),
                'trade_id': trade.id,
                'message': 'Limit order placed successfully'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def place_market_order(self, user_id: int, market_id: str, outcome: str, 
                               side: str, shares: float, 
                               slippage_tolerance: float = 0.10) -> Dict:
        """Place a market order."""
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        wallet = self.wallet_service.get_user_wallet(user_id)
        
        if not user or not wallet:
            return {'success': False, 'error': 'User or wallet not found'}
        
        try:
            # Get current market price
            market_data = await self.clob_api.get_market_prices(market_id)
            current_price = market_data.get('yes_price' if outcome == 'YES' else 'no_price', 0)
            
            # Apply slippage protection
            if side.upper() == 'BUY':
                max_price = current_price * (1 + slippage_tolerance)
            else:
                max_price = current_price * (1 - slippage_tolerance)
            
            # Prepare order data
            order_data = {
                'market_id': market_id,
                'outcome': outcome,
                'side': side.upper(),
                'shares': shares,
                'max_price': max_price,
                'slippage_tolerance': slippage_tolerance,
                'wallet_address': wallet.address
            }
            
            # Place order via Gamma API
            result = await self.gamma_api.place_market_order(order_data)
            
            # Create trade record
            trade = Trade(
                user_id=user_id,
                market_id=market_id,
                outcome=outcome,
                side=side.upper(),
                order_type='MARKET',
                shares=shares,
                price=max_price,
                total_amount=shares * max_price,
                status='pending',
                order_id=result.get('order_id')
            )
            
            db.add(trade)
            db.commit()
            
            return {
                'success': True,
                'order_id': result.get('order_id'),
                'trade_id': trade.id,
                'message': 'Market order placed successfully'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def cancel_order(self, user_id: int, order_id: str) -> Dict:
        """Cancel an order."""
        db = next(get_db())
        trade = db.query(Trade).filter(Trade.order_id == order_id, Trade.user_id == user_id).first()
        
        if not trade:
            return {'success': False, 'error': 'Order not found'}
        
        try:
            # Cancel order via Gamma API
            result = await self.gamma_api.cancel_order(order_id)
            
            # Update trade status
            trade.status = 'cancelled'
            db.commit()
            
            return {
                'success': True,
                'message': 'Order cancelled successfully'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def get_user_orders(self, user_id: int, status: str = None) -> List[Dict]:
        """Get user's orders."""
        db = next(get_db())
        query = db.query(Trade).filter(Trade.user_id == user_id)
        
        if status:
            query = query.filter(Trade.status == status)
        
        trades = query.order_by(Trade.created_at.desc()).all()
        
        return [
            {
                'id': trade.id,
                'market_id': trade.market_id,
                'outcome': trade.outcome,
                'side': trade.side,
                'order_type': trade.order_type,
                'shares': trade.shares,
                'price': trade.price,
                'total_amount': trade.total_amount,
                'status': trade.status,
                'created_at': trade.created_at.isoformat(),
                'filled_at': trade.filled_at.isoformat() if trade.filled_at else None
            }
            for trade in trades
        ]
    
    async def update_positions(self, user_id: int) -> Dict:
        """Update user's positions from Polymarket."""
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        wallet = self.wallet_service.get_user_wallet(user_id)
        
        if not user or not wallet:
            return {'success': False, 'error': 'User or wallet not found'}
        
        try:
            # Get positions from Polymarket Data API
            positions_data = await self.data_api.get_user_positions(wallet.address)
            
            # Update or create positions in database
            for pos_data in positions_data:
                position = db.query(Position).filter(
                    Position.user_id == user_id,
                    Position.market_id == pos_data.get('market_id')
                ).first()
                
                if position:
                    # Update existing position
                    position.shares = pos_data.get('shares', 0)
                    position.current_price = pos_data.get('current_price', 0)
                    position.unrealized_pnl = pos_data.get('unrealized_pnl', 0)
                    position.updated_at = datetime.utcnow()
                else:
                    # Create new position
                    position = Position(
                        user_id=user_id,
                        market_id=pos_data.get('market_id'),
                        market_title=pos_data.get('market_title', ''),
                        outcome=pos_data.get('outcome', ''),
                        shares=pos_data.get('shares', 0),
                        average_price=pos_data.get('average_price', 0),
                        current_price=pos_data.get('current_price', 0),
                        unrealized_pnl=pos_data.get('unrealized_pnl', 0)
                    )
                    db.add(position)
            
            db.commit()
            
            return {
                'success': True,
                'message': f'Updated {len(positions_data)} positions'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def get_market_info(self, market_id: str) -> Dict:
        """Get detailed market information."""
        try:
            # Get market details from Gamma API
            market_details = await self.gamma_api.get_market_details(market_id)
            
            # Get orderbook from CLOB API
            orderbook = await self.clob_api.get_orderbook(market_id)
            
            # Get recent trades
            recent_trades = await self.clob_api.get_recent_trades(market_id, limit=10)
            
            return {
                'success': True,
                'market': market_details,
                'orderbook': orderbook,
                'recent_trades': recent_trades
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def calculate_slippage(self, market_id: str, side: str, shares: float) -> Dict:
        """Calculate expected slippage for an order."""
        try:
            orderbook = await self.clob_api.get_orderbook(market_id)
            
            # Calculate slippage based on orderbook depth
            # This is a simplified calculation
            if side.upper() == 'BUY':
                asks = orderbook.get('asks', [])
                total_volume = sum([ask['size'] for ask in asks])
                if total_volume >= shares:
                    slippage = 0.01  # 1% if sufficient liquidity
                else:
                    slippage = 0.05  # 5% if insufficient liquidity
            else:
                bids = orderbook.get('bids', [])
                total_volume = sum([bid['size'] for bid in bids])
                if total_volume >= shares:
                    slippage = 0.01  # 1% if sufficient liquidity
                else:
                    slippage = 0.05  # 5% if insufficient liquidity
            
            return {
                'success': True,
                'expected_slippage': slippage,
                'sufficient_liquidity': total_volume >= shares
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

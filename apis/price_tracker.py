import aiohttp
import asyncio
import websockets
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from config import Config

class PriceTracker:
    """Price tracking service for tokens and markets."""
    
    def __init__(self):
        self.prices = {}
        self.subscribers = []
        self.is_running = False
    
    async def get_token_price(self, symbol: str) -> Optional[Dict]:
        """Get current price for a token."""
        # This would typically fetch from a price API like CoinGecko or CoinMarketCap
        # For now, we'll use a mock implementation
        price_apis = {
            'POL': 'https://api.coingecko.com/api/v3/simple/price?ids=polymarket&vs_currencies=usd',
            'ETH': 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd',
            'SOL': 'https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd',
            'USDC': 'https://api.coingecko.com/api/v3/simple/price?ids=usd-coin&vs_currencies=usd'
        }
        
        if symbol not in price_apis:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(price_apis[symbol]) as response:
                    if response.status == 200:
                        data = await response.json()
                        token_id = 'polymarket' if symbol == 'POL' else symbol.lower()
                        if symbol == 'USDC':
                            token_id = 'usd-coin'
                        elif symbol == 'ETH':
                            token_id = 'ethereum'
                        elif symbol == 'SOL':
                            token_id = 'solana'
                        
                        price_data = data.get(token_id, {})
                        return {
                            'symbol': symbol,
                            'price_usd': price_data.get('usd', 0),
                            'timestamp': datetime.utcnow().isoformat()
                        }
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    async def get_multiple_prices(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get prices for multiple tokens."""
        prices = {}
        tasks = [self.get_token_price(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for symbol, result in zip(symbols, results):
            if isinstance(result, dict):
                prices[symbol] = result
            else:
                prices[symbol] = {
                    'symbol': symbol,
                    'price_usd': 0,
                    'timestamp': datetime.utcnow().isoformat(),
                    'error': str(result)
                }
        
        return prices
    
    async def start_price_tracking(self, symbols: List[str], interval: int = 30):
        """Start continuous price tracking."""
        self.is_running = True
        
        while self.is_running:
            try:
                prices = await self.get_multiple_prices(symbols)
                self.prices.update(prices)
                
                # Notify subscribers
                for callback in self.subscribers:
                    try:
                        await callback(prices)
                    except Exception as e:
                        print(f"Error in price callback: {e}")
                
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in price tracking: {e}")
                await asyncio.sleep(interval)
    
    def stop_price_tracking(self):
        """Stop price tracking."""
        self.is_running = False
    
    def subscribe_to_prices(self, callback: Callable):
        """Subscribe to price updates."""
        self.subscribers.append(callback)
    
    def unsubscribe_from_prices(self, callback: Callable):
        """Unsubscribe from price updates."""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def get_cached_price(self, symbol: str) -> Optional[Dict]:
        """Get cached price for a symbol."""
        return self.prices.get(symbol)
    
    def get_all_cached_prices(self) -> Dict[str, Dict]:
        """Get all cached prices."""
        return self.prices.copy()
    
    async def get_market_price(self, market_id: str) -> Optional[Dict]:
        """Get current price for a Polymarket market."""
        # This would integrate with Polymarket CLOB API
        # For now, return a mock implementation
        return {
            'market_id': market_id,
            'yes_price': 0.65,
            'no_price': 0.35,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def get_portfolio_value(self, positions: List[Dict], token_prices: Dict[str, Dict]) -> float:
        """Calculate total portfolio value."""
        total_value = 0.0
        
        for position in positions:
            market_id = position.get('market_id')
            shares = position.get('shares', 0)
            outcome = position.get('outcome')
            
            # Get market price
            market_price = await self.get_market_price(market_id)
            if market_price:
                if outcome == 'YES':
                    price = market_price.get('yes_price', 0)
                else:
                    price = market_price.get('no_price', 0)
                
                total_value += shares * price
        
        return total_value

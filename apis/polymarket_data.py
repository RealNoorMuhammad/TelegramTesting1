import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from config import Config

class PolymarketDataAPI:
    """Polymarket Data API client for positions, trades, and portfolio."""
    
    def __init__(self):
        self.base_url = Config.POLYMARKET_DATA_API_URL
        self.api_key = Config.POLYMARKET_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    async def get_user_positions(self, user_address: str) -> List[Dict]:
        """Get user's positions."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/positions/{user_address}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"Positions fetch failed: {response.status}")
    
    async def get_user_trades(self, user_address: str, limit: int = 100) -> List[Dict]:
        """Get user's trade history."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/trades/{user_address}"
            params = {'limit': limit}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"Trades fetch failed: {response.status}")
    
    async def get_user_portfolio(self, user_address: str) -> Dict:
        """Get user's portfolio summary."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/portfolio/{user_address}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Portfolio fetch failed: {response.status}")
    
    async def get_position_details(self, position_id: str) -> Dict:
        """Get detailed position information."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/positions/details/{position_id}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Position details fetch failed: {response.status}")
    
    async def get_trade_details(self, trade_id: str) -> Dict:
        """Get detailed trade information."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/trades/details/{trade_id}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Trade details fetch failed: {response.status}")
    
    async def get_user_pnl(self, user_address: str, timeframe: str = 'all') -> Dict:
        """Get user's PnL data."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/pnl/{user_address}"
            params = {'timeframe': timeframe}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"PnL fetch failed: {response.status}")
    
    async def get_market_volume(self, market_id: str, timeframe: str = '24h') -> Dict:
        """Get market volume data."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}/volume"
            params = {'timeframe': timeframe}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Market volume fetch failed: {response.status}")

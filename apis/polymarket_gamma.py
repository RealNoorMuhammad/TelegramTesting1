import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from config import Config

class PolymarketGammaAPI:
    """Polymarket Gamma API client for events, markets, sports, search, and orders."""
    
    def __init__(self):
        self.base_url = Config.POLYMARKET_GAMMA_API_URL
        self.api_key = Config.POLYMARKET_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    async def search_markets(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for markets by query."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/search"
            params = {
                'query': query,
                'limit': limit,
                'active': True
            }
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"Search failed: {response.status}")
    
    async def get_market_details(self, market_id: str) -> Dict:
        """Get detailed information about a specific market."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Market details failed: {response.status}")
    
    async def get_events(self, limit: int = 50) -> List[Dict]:
        """Get list of events."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/events"
            params = {'limit': limit, 'active': True}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"Events fetch failed: {response.status}")
    
    async def get_sports_events(self, sport: str = None) -> List[Dict]:
        """Get sports events."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/sports/events"
            params = {}
            if sport:
                params['sport'] = sport
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"Sports events fetch failed: {response.status}")
    
    async def place_limit_order(self, order_data: Dict) -> Dict:
        """Place a limit order."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/orders/limit"
            
            async with session.post(url, headers=self.headers, json=order_data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_data = await response.json()
                    raise Exception(f"Limit order failed: {error_data}")
    
    async def place_market_order(self, order_data: Dict) -> Dict:
        """Place a market order."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/orders/market"
            
            async with session.post(url, headers=self.headers, json=order_data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_data = await response.json()
                    raise Exception(f"Market order failed: {error_data}")
    
    async def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/orders/{order_id}/cancel"
            
            async with session.post(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_data = await response.json()
                    raise Exception(f"Cancel order failed: {error_data}")
    
    async def get_user_orders(self, user_address: str, status: str = None) -> List[Dict]:
        """Get user's orders."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/orders/user/{user_address}"
            params = {}
            if status:
                params['status'] = status
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"User orders fetch failed: {response.status}")
    
    async def get_order_status(self, order_id: str) -> Dict:
        """Get order status."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/orders/{order_id}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Order status fetch failed: {response.status}")

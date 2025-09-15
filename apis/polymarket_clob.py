import aiohttp
import asyncio
import websockets
import json
from typing import Dict, List, Optional, Any, Callable
from config import Config

class PolymarketCLOBAPI:
    """Polymarket CLOB API client for orderbook and prices."""
    
    def __init__(self):
        self.base_url = Config.POLYMARKET_CLOB_API_URL
        self.ws_url = Config.WEBSOCKET_URL
        self.api_key = Config.POLYMARKET_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    async def get_orderbook(self, market_id: str) -> Dict:
        """Get orderbook for a market."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/orderbook/{market_id}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Orderbook fetch failed: {response.status}")
    
    async def get_market_prices(self, market_id: str) -> Dict:
        """Get current market prices."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}/prices"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Market prices fetch failed: {response.status}")
    
    async def get_ticker(self, market_id: str) -> Dict:
        """Get market ticker data."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/ticker/{market_id}"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Ticker fetch failed: {response.status}")
    
    async def get_recent_trades(self, market_id: str, limit: int = 50) -> List[Dict]:
        """Get recent trades for a market."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}/trades"
            params = {'limit': limit}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    raise Exception(f"Recent trades fetch failed: {response.status}")
    
    async def get_market_stats(self, market_id: str) -> Dict:
        """Get market statistics."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}/stats"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Market stats fetch failed: {response.status}")
    
    async def subscribe_to_orderbook(self, market_id: str, callback: Callable):
        """Subscribe to orderbook updates via WebSocket."""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Subscribe to orderbook updates
                subscribe_message = {
                    "type": "subscribe",
                    "channel": "orderbook",
                    "market": market_id
                }
                
                await websocket.send(json.dumps(subscribe_message))
                
                async for message in websocket:
                    data = json.loads(message)
                    await callback(data)
                    
        except Exception as e:
            print(f"WebSocket connection error: {e}")
    
    async def subscribe_to_trades(self, market_id: str, callback: Callable):
        """Subscribe to trade updates via WebSocket."""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Subscribe to trade updates
                subscribe_message = {
                    "type": "subscribe",
                    "channel": "trades",
                    "market": market_id
                }
                
                await websocket.send(json.dumps(subscribe_message))
                
                async for message in websocket:
                    data = json.loads(message)
                    await callback(data)
                    
        except Exception as e:
            print(f"WebSocket connection error: {e}")
    
    async def subscribe_to_prices(self, market_ids: List[str], callback: Callable):
        """Subscribe to price updates for multiple markets."""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Subscribe to price updates for multiple markets
                for market_id in market_ids:
                    subscribe_message = {
                        "type": "subscribe",
                        "channel": "prices",
                        "market": market_id
                    }
                    await websocket.send(json.dumps(subscribe_message))
                
                async for message in websocket:
                    data = json.loads(message)
                    await callback(data)
                    
        except Exception as e:
            print(f"WebSocket connection error: {e}")
    
    async def get_market_depth(self, market_id: str) -> Dict:
        """Get market depth (bids and asks)."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}/depth"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Market depth fetch failed: {response.status}")
    
    async def get_best_bid_ask(self, market_id: str) -> Dict:
        """Get best bid and ask prices."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/markets/{market_id}/best"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Best bid/ask fetch failed: {response.status}")

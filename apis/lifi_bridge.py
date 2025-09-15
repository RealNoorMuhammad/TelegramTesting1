import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from config import Config

class LifiBridgeAPI:
    """LI.FI Bridge API client for cross-chain token transfers."""
    
    def __init__(self):
        self.base_url = Config.LIFI_API_URL
        self.api_key = Config.LIFI_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    async def get_chains(self) -> List[Dict]:
        """Get supported chains."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/chains"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('chains', [])
                else:
                    raise Exception(f"Chains fetch failed: {response.status}")
    
    async def get_tokens(self, chain_id: int) -> List[Dict]:
        """Get tokens for a specific chain."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/tokens"
            params = {'chain': chain_id}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('tokens', [])
                else:
                    raise Exception(f"Tokens fetch failed: {response.status}")
    
    async def get_quote(self, from_chain: int, to_chain: int, from_token: str, 
                       to_token: str, amount: str, from_address: str) -> Dict:
        """Get a quote for a cross-chain swap."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/quote"
            params = {
                'fromChain': from_chain,
                'toChain': to_chain,
                'fromToken': from_token,
                'toToken': to_token,
                'amount': amount,
                'fromAddress': from_address
            }
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_data = await response.json()
                    raise Exception(f"Quote failed: {error_data}")
    
    async def get_routes(self, from_chain: int, to_chain: int, from_token: str, 
                        to_token: str, amount: str, from_address: str) -> List[Dict]:
        """Get available routes for a cross-chain swap."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/routes"
            params = {
                'fromChain': from_chain,
                'toChain': to_chain,
                'fromToken': from_token,
                'toToken': to_token,
                'amount': amount,
                'fromAddress': from_address
            }
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('routes', [])
                else:
                    raise Exception(f"Routes fetch failed: {response.status}")
    
    async def get_status(self, tx_hash: str) -> Dict:
        """Get status of a bridge transaction."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/status"
            params = {'txHash': tx_hash}
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Status fetch failed: {response.status}")
    
    async def get_balance(self, chain_id: int, token_address: str, wallet_address: str) -> Dict:
        """Get token balance for a wallet."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/balance"
            params = {
                'chain': chain_id,
                'tokenAddress': token_address,
                'walletAddress': wallet_address
            }
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Balance fetch failed: {response.status}")
    
    async def get_approval(self, chain_id: int, token_address: str, amount: str) -> Dict:
        """Get approval transaction for a token."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/approval"
            params = {
                'chain': chain_id,
                'tokenAddress': token_address,
                'amount': amount
            }
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Approval fetch failed: {response.status}")
    
    async def get_swap_quote(self, from_chain: int, to_chain: int, from_token: str, 
                            to_token: str, amount: str, from_address: str, 
                            slippage: float = 0.01) -> Dict:
        """Get a detailed swap quote with slippage."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/quote"
            params = {
                'fromChain': from_chain,
                'toChain': to_chain,
                'fromToken': from_token,
                'toToken': to_token,
                'amount': amount,
                'fromAddress': from_address,
                'slippage': slippage
            }
            
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_data = await response.json()
                    raise Exception(f"Swap quote failed: {error_data}")

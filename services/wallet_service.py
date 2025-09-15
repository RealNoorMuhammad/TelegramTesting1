from typing import Optional, Dict, List
from eth_account import Account
from web3 import Web3
from database import get_db, User, Wallet
from database.encryption import encrypt_private_key, decrypt_private_key
from apis import LifiBridgeAPI
import secrets

class WalletService:
    """Service for wallet management and operations."""
    
    def __init__(self):
        self.lifi_api = LifiBridgeAPI()
    
    def generate_wallet(self) -> Dict[str, str]:
        """Generate a new Ethereum wallet."""
        account = Account.create()
        return {
            'address': account.address,
            'private_key': account.key.hex()
        }
    
    def create_wallet_for_user(self, user_id: int, network: str = 'polygon') -> Optional[Wallet]:
        """Create a new wallet for a user."""
        db = next(get_db())
        
        # Generate new wallet
        wallet_data = self.generate_wallet()
        
        # Encrypt private key
        encrypted_private_key = encrypt_private_key(wallet_data['private_key'])
        
        # Create wallet record
        wallet = Wallet(
            user_id=user_id,
            address=wallet_data['address'],
            encrypted_private_key=encrypted_private_key,
            network=network
        )
        
        db.add(wallet)
        db.commit()
        
        return wallet
    
    def get_user_wallet(self, user_id: int) -> Optional[Wallet]:
        """Get user's active wallet."""
        db = next(get_db())
        return db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.is_active == True).first()
    
    def get_wallet_balance(self, wallet_address: str, token_address: str = None) -> Dict[str, float]:
        """Get wallet balance for different tokens."""
        # In a real implementation, this would connect to the blockchain
        # For now, return mock data
        return {
            'POL': 1000.0,
            'USDC': 500.0,
            'ETH': 0.5
        }
    
    def send_tokens(self, from_wallet: Wallet, to_address: str, amount: float, token: str) -> Dict:
        """Send tokens from user's wallet."""
        # Decrypt private key
        private_key = decrypt_private_key(from_wallet.encrypted_private_key)
        
        # In a real implementation, this would create and sign a transaction
        # For now, return mock success
        return {
            'success': True,
            'transaction_hash': '0x' + secrets.token_hex(32),
            'amount': amount,
            'token': token,
            'to_address': to_address
        }
    
    async def bridge_tokens(self, from_wallet: Wallet, to_chain: int, token: str, amount: float) -> Dict:
        """Bridge tokens to another chain using LI.FI."""
        try:
            # Get quote for bridge
            quote = await self.lifi_api.get_quote(
                from_chain=137,  # Polygon
                to_chain=to_chain,
                from_token=token,
                to_token=token,
                amount=str(amount),
                from_address=from_wallet.address
            )
            
            return {
                'success': True,
                'quote': quote,
                'estimated_time': quote.get('estimatedTime', 'Unknown'),
                'fee': quote.get('fee', 0)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_transaction_history(self, wallet_address: str) -> List[Dict]:
        """Get transaction history for a wallet."""
        # In a real implementation, this would fetch from blockchain
        # For now, return mock data
        return [
            {
                'hash': '0x' + secrets.token_hex(32),
                'type': 'send',
                'amount': 100.0,
                'token': 'POL',
                'to': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
                'timestamp': '2024-01-15T10:30:00Z',
                'status': 'confirmed'
            },
            {
                'hash': '0x' + secrets.token_hex(32),
                'type': 'receive',
                'amount': 50.0,
                'token': 'USDC',
                'from': '0x8ba1f109551bD432803012645Hac136c',
                'timestamp': '2024-01-15T09:15:00Z',
                'status': 'confirmed'
            }
        ]
    
    def validate_address(self, address: str) -> bool:
        """Validate if an address is a valid Ethereum address."""
        try:
            return Web3.is_address(address)
        except:
            return False

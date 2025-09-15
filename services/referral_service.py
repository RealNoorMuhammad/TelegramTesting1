from typing import Dict, List, Optional
from database import get_db, User, ReferralReward
from services.trading_service import TradingService
import secrets
import string

class ReferralService:
    """Service for referral system management."""
    
    def __init__(self):
        self.trading_service = TradingService()
    
    def generate_referral_code(self) -> str:
        """Generate a unique referral code."""
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    def create_referral_link(self, user_id: int) -> str:
        """Create referral link for a user."""
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        if not user.referral_code:
            user.referral_code = self.generate_referral_code()
            db.commit()
        
        return f"https://t.me/your_bot?start={user.referral_code}"
    
    def process_referral(self, referrer_code: str, new_user_id: int) -> Dict:
        """Process a new referral."""
        db = next(get_db())
        
        # Find referrer by code
        referrer = db.query(User).filter(User.referral_code == referrer_code).first()
        if not referrer:
            return {'success': False, 'error': 'Invalid referral code'}
        
        # Check if user already has a referrer
        new_user = db.query(User).filter(User.id == new_user_id).first()
        if new_user.referrer_id:
            return {'success': False, 'error': 'User already has a referrer'}
        
        # Set referrer
        new_user.referrer_id = referrer.id
        db.commit()
        
        # Create referral reward record
        reward = ReferralReward(
            referrer_id=referrer.id,
            referred_id=new_user_id,
            reward_amount=0.0,  # Will be calculated when referred user trades
            reward_type='commission'
        )
        db.add(reward)
        db.commit()
        
        return {
            'success': True,
            'referrer_id': referrer.id,
            'message': 'Referral processed successfully'
        }
    
    def get_referral_stats(self, user_id: int) -> Dict:
        """Get referral statistics for a user."""
        db = next(get_db())
        
        # Count direct referrals
        direct_referrals = db.query(User).filter(User.referrer_id == user_id).count()
        
        # Count total referrals in the tree (recursive)
        total_referrals = self._count_total_referrals(user_id)
        
        # Calculate total rewards earned
        total_rewards = db.query(ReferralReward).filter(
            ReferralReward.referrer_id == user_id,
            ReferralReward.status == 'paid'
        ).with_entities(ReferralReward.reward_amount).all()
        
        total_earned = sum([reward[0] for reward in total_rewards])
        
        # Get pending rewards
        pending_rewards = db.query(ReferralReward).filter(
            ReferralReward.referrer_id == user_id,
            ReferralReward.status == 'pending'
        ).with_entities(ReferralReward.reward_amount).all()
        
        pending_earned = sum([reward[0] for reward in pending_rewards])
        
        return {
            'direct_referrals': direct_referrals,
            'total_referrals': total_referrals,
            'total_earned': total_earned,
            'pending_earned': pending_earned
        }
    
    def _count_total_referrals(self, user_id: int) -> int:
        """Recursively count total referrals in the tree."""
        db = next(get_db())
        direct_referrals = db.query(User).filter(User.referrer_id == user_id).all()
        
        total = len(direct_referrals)
        for referral in direct_referrals:
            total += self._count_total_referrals(referral.id)
        
        return total
    
    def get_referral_tree(self, user_id: int, depth: int = 3) -> Dict:
        """Get referral tree structure."""
        db = next(get_db())
        
        def build_tree(user_id, current_depth):
            if current_depth >= depth:
                return None
            
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            referrals = db.query(User).filter(User.referrer_id == user_id).all()
            
            tree = {
                'user_id': user.id,
                'username': user.username,
                'referral_code': user.referral_code,
                'referrals': []
            }
            
            for referral in referrals:
                referral_tree = build_tree(referral.id, current_depth + 1)
                if referral_tree:
                    tree['referrals'].append(referral_tree)
            
            return tree
        
        return build_tree(user_id, 0)
    
    def calculate_referral_reward(self, trade_amount: float, commission_rate: float = 0.10) -> float:
        """Calculate referral reward for a trade."""
        return trade_amount * commission_rate
    
    def process_trade_reward(self, user_id: int, trade_amount: float) -> Dict:
        """Process referral reward when a user makes a trade."""
        db = next(get_db())
        
        # Find all referrers in the chain
        referrers = self._get_referrer_chain(user_id)
        
        total_processed = 0
        for referrer_id in referrers:
            # Calculate reward (10% commission)
            reward_amount = self.calculate_referral_reward(trade_amount)
            
            # Create or update reward record
            reward = db.query(ReferralReward).filter(
                ReferralReward.referrer_id == referrer_id,
                ReferralReward.referred_id == user_id
            ).first()
            
            if reward:
                reward.reward_amount += reward_amount
            else:
                reward = ReferralReward(
                    referrer_id=referrer_id,
                    referred_id=user_id,
                    reward_amount=reward_amount,
                    reward_type='commission'
                )
                db.add(reward)
            
            total_processed += 1
        
        db.commit()
        
        return {
            'success': True,
            'referrers_rewarded': total_processed,
            'total_reward': trade_amount * 0.10 * total_processed
        }
    
    def _get_referrer_chain(self, user_id: int) -> List[int]:
        """Get the chain of referrers for a user."""
        db = next(get_db())
        referrers = []
        
        user = db.query(User).filter(User.id == user_id).first()
        while user and user.referrer_id:
            referrers.append(user.referrer_id)
            user = db.query(User).filter(User.id == user.referrer_id).first()
        
        return referrers
    
    def get_referral_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get referral leaderboard."""
        db = next(get_db())
        
        # Get users with most referrals
        top_referrers = db.query(
            User.id,
            User.username,
            User.referral_code
        ).join(ReferralReward, User.id == ReferralReward.referrer_id).group_by(
            User.id
        ).order_by(
            db.func.sum(ReferralReward.reward_amount).desc()
        ).limit(limit).all()
        
        leaderboard = []
        for i, (user_id, username, referral_code) in enumerate(top_referrers):
            stats = self.get_referral_stats(user_id)
            leaderboard.append({
                'rank': i + 1,
                'user_id': user_id,
                'username': username,
                'referral_code': referral_code,
                'total_referrals': stats['total_referrals'],
                'total_earned': stats['total_earned']
            })
        
        return leaderboard

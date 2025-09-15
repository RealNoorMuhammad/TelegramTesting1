#!/usr/bin/env python3
"""
PolyFocus Telegram Trading Bot
A comprehensive trading bot for Polymarket with advanced features.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import Config
from database import init_db
from bot.main import main as run_bot
from apis.price_tracker import PriceTracker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('polymarket_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class PolyFocusBot:
    """Main application class for PolyFocus Bot."""
    
    def __init__(self):
        self.price_tracker = PriceTracker()
        self.is_running = False
    
    async def start(self):
        """Start the bot and all services."""
        logger.info("Starting PolyFocus Bot...")
        
        try:
            # Initialize database
            logger.info("Initializing database...")
            init_db()
            
            # Start price tracking
            logger.info("Starting price tracking...")
            price_task = asyncio.create_task(
                self.price_tracker.start_price_tracking(['POL', 'USDC', 'ETH'], interval=30)
            )
            
            # Start Telegram bot
            logger.info("Starting Telegram bot...")
            bot_task = asyncio.create_task(self._run_bot())
            
            self.is_running = True
            
            # Wait for tasks
            await asyncio.gather(price_task, bot_task)
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    async def _run_bot(self):
        """Run the Telegram bot."""
        try:
            # Import and run the bot in a separate thread to avoid event loop conflicts
            import threading
            import asyncio
            
            def run_bot_sync():
                asyncio.run(run_bot())
            
            bot_thread = threading.Thread(target=run_bot_sync)
            bot_thread.daemon = True
            bot_thread.start()
            bot_thread.join()
        except Exception as e:
            logger.error(f"Bot error: {e}")
            raise
    
    def stop(self):
        """Stop the bot and all services."""
        logger.info("Stopping PolyFocus Bot...")
        self.is_running = False
        self.price_tracker.stop_price_tracking()

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)

async def main():
    """Main entry point."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start bot
    bot = PolyFocusBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        bot.stop()

if __name__ == '__main__':
    # Check if required environment variables are set
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
        sys.exit(1)
    
    if not Config.ENCRYPTION_KEY:
        logger.error("ENCRYPTION_KEY not set in environment variables")
        sys.exit(1)
    
    # Run the bot
    asyncio.run(main())

"""
Health check endpoint for PolyFocus Bot
"""

from flask import Flask, jsonify
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        db_path = os.getenv('DATABASE_URL', 'sqlite:///./polymarket_bot.db')
        if db_path.startswith('sqlite:///'):
            db_file = db_path.replace('sqlite:///', '')
            if os.path.exists(db_file):
                conn = sqlite3.connect(db_file)
                conn.execute('SELECT 1')
                conn.close()
                db_status = 'healthy'
            else:
                db_status = 'unhealthy - database file not found'
        else:
            db_status = 'healthy - using external database'
        
        # Check if required environment variables are set
        required_vars = ['TELEGRAM_BOT_TOKEN', 'ENCRYPTION_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            config_status = f'unhealthy - missing variables: {", ".join(missing_vars)}'
        else:
            config_status = 'healthy'
        
        # Overall health status
        overall_status = 'healthy' if db_status == 'healthy' and config_status == 'healthy' else 'unhealthy'
        
        return jsonify({
            'status': overall_status,
            'database': db_status,
            'configuration': config_status,
            'version': '1.0.0',
            'service': 'polyfocus-bot'
        }), 200 if overall_status == 'healthy' else 503
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'version': '1.0.0',
            'service': 'polyfocus-bot'
        }), 503

@app.route('/')
def root():
    """Root endpoint."""
    return jsonify({
        'message': 'PolyFocus Bot API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'docs': 'https://docs.polyfocus.com'
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

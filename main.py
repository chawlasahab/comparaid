from app import create_app, db
from scheduler import start_scheduler
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = create_app()

def init_db():
    """Initialize database tables and stores"""
    with app.app_context():
        db.create_all()
        
        # Initialize stores if they don't exist
        from app.models import Store
        stores_data = [
            {'name': 'Tesco', 'website': 'https://www.tesco.ie'},
            {'name': 'SuperValu', 'website': 'https://shop.supervalu.ie'},
            {'name': 'Dunnes', 'website': 'https://www.dunnesstores.com'},
            {'name': 'Lidl', 'website': 'https://www.lidl.ie'},
            {'name': 'Aldi', 'website': 'https://www.aldi.ie'}
        ]
        
        for store_data in stores_data:
            if not Store.query.filter_by(name=store_data['name']).first():
                store = Store(**store_data)
                db.session.add(store)
        
        db.session.commit()

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start background scheduler in production
    if os.getenv('FLASK_ENV') != 'development':
        start_scheduler()
    
    # Run Flask app
    port = int(os.getenv('PORT', 8765))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
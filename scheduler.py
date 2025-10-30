from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app, db
from app.models import Product, Store, PriceHistory
from app.scraper import TescoScraper, SuperValuScraper, DunnesScraper, LidlScraper, AldiScraper
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceUpdateScheduler:
    def __init__(self):
        self.app = create_app()
        self.scrapers = {
            'Tesco': TescoScraper(),
            'SuperValu': SuperValuScraper(),
            'Dunnes': DunnesScraper(),
            'Lidl': LidlScraper(),
            'Aldi': AldiScraper()
        }
        # Comprehensive grocery categories for complete data collection
        self.comprehensive_categories = [
            'milk', 'bread', 'eggs', 'butter', 'cheese', 'yogurt',
            'chicken', 'beef', 'pork', 'fish', 'bacon', 'sausages',
            'apples', 'bananas', 'oranges', 'grapes', 'strawberries',
            'potatoes', 'onions', 'carrots', 'tomatoes', 'lettuce',
            'pasta', 'rice', 'cereal', 'flour', 'sugar', 'oil',
            'coffee', 'tea', 'juice', 'water', 'wine', 'beer',
            'soap', 'shampoo', 'toothpaste', 'detergent', 'tissues'
        ]
        # Scraping every 2 days (48 hours) for legal compliance
    
    def update_prices(self):
        """Update prices for all popular items across all stores"""
        with self.app.app_context():
            logger.info("Starting price update job")
            
            for category in self.comprehensive_categories:
                self._update_item_prices(category)
            
            logger.info("Price update job completed")
    
    def _update_item_prices(self, item):
        """Update prices for a specific item across all stores"""
        logger.info(f"Updating prices for: {item}")
        
        with self.app.app_context():
            for store_name, scraper in self.scrapers.items():
                try:
                    # Get store from database
                    store = Store.query.filter_by(name=store_name).first()
                    if not store:
                        store = Store(name=store_name, is_active=True, scraper_enabled=True)
                        db.session.add(store)
                        db.session.commit()
                    
                    # Scrape products
                    products_data = scraper.search_products(item)
                    
                    for product_data in products_data:
                        self._save_product(product_data, store.id, item)
                    
                    # Update last scraped time
                    store.last_scraped = datetime.utcnow()
                    db.session.commit()
                    
                    logger.info(f"Updated {len(products_data)} products for {store_name}")
                    
                except Exception as e:
                    logger.error(f"Error updating {store_name} for {item}: {e}")
    
    def _save_product(self, product_data, store_id, search_term):
        """Save or update product in database"""
        try:
            # Check if product exists
            existing = Product.query.filter_by(
                name=product_data['product'],
                store_id=store_id
            ).first()
            
            if existing:
                # Update existing product
                old_price = existing.price
                existing.price = product_data['price']
                existing.last_updated = datetime.utcnow()
                existing.is_active = True
                
                # Record price history if price changed
                if old_price != product_data['price']:
                    PriceHistory.record_price(existing.id, product_data['price'])
            else:
                # Create new product
                product = Product(
                    name=product_data['product'],
                    store_id=store_id,
                    price=product_data['price'],
                    unit=product_data['unit'],
                    image_url=product_data['image'],
                    store_url=product_data['url'],
                    search_term=search_term.lower(),
                    is_active=True
                )
                db.session.add(product)
                db.session.flush()  # Get the ID
                
                # Record initial price
                PriceHistory.record_price(product.id, product_data['price'])
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error saving product {product_data['product']}: {e}")
            db.session.rollback()

def start_scheduler():
    """Start the background scheduler"""
    scheduler = BackgroundScheduler()
    price_updater = PriceUpdateScheduler()
    
    # Schedule price updates every 2 days (48 hours)
    scheduler.add_job(
        func=price_updater.update_prices,
        trigger="interval",
        hours=48,
        id='price_update_job'
    )
    
    # Run initial update
    scheduler.add_job(
        func=price_updater.update_prices,
        trigger="date",
        run_date=datetime.now(),
        id='initial_price_update'
    )
    
    scheduler.start()
    logger.info("Price update scheduler started")
    return scheduler

if __name__ == '__main__':
    scheduler = start_scheduler()
    try:
        # Keep the script running
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class SuperValuScraper(BaseScraper):
    def __init__(self):
        super().__init__('SuperValu', delay=2.0)
        self.base_url = 'https://shop.supervalu.ie'
    
    def search_products(self, query: str):
        """Search SuperValu for products"""
        logger.info(f"Searching SuperValu for: {query}")
        return self._get_mock_products(query)
    
    def _get_mock_products(self, query: str):
        """Generate realistic mock data for SuperValu"""
        import random
        
        # Use same comprehensive database with SuperValu pricing (5% higher than Tesco)
        base_products = {
            'milk': [
                {'name': 'SuperValu Fresh Milk 1L', 'price': 1.31, 'unit': '1L'},
                {'name': 'SuperValu Fresh Milk 2L', 'price': 2.26, 'unit': '2L'},
                {'name': 'SuperValu Organic Milk 1L', 'price': 1.95, 'unit': '1L'},
                {'name': 'SuperValu Skimmed Milk 1L', 'price': 1.31, 'unit': '1L'},
                {'name': 'SuperValu Whole Milk 500ml', 'price': 0.79, 'unit': '500ml'},
                {'name': 'SuperValu Lactose Free Milk 1L', 'price': 2.05, 'unit': '1L'}
            ],
            'bread': [{'name': 'SuperValu White Bread', 'price': 1.15, 'unit': '800g'}, {'name': 'SuperValu Brown Bread', 'price': 1.35, 'unit': '800g'}],
            'eggs': [{'name': 'SuperValu Free Range Eggs 12pk', 'price': 3.45, 'unit': '12 pack'}],
            'butter': [{'name': 'SuperValu Irish Butter 500g', 'price': 2.99, 'unit': '500g'}],
            'chicken': [{'name': 'SuperValu Chicken Breast 500g', 'price': 4.46, 'unit': '500g'}],
            'bananas': [{'name': 'SuperValu Bananas 1kg', 'price': 1.56, 'unit': '1kg'}],
            'apples': [{'name': 'SuperValu Apples 1kg', 'price': 2.40, 'unit': '1kg'}],
            'cheese': [{'name': 'SuperValu Cheddar Cheese 200g', 'price': 2.63, 'unit': '200g'}],
            'yogurt': [{'name': 'SuperValu Natural Yogurt 500g', 'price': 1.84, 'unit': '500g'}],
            'pasta': [{'name': 'SuperValu Spaghetti 500g', 'price': 0.89, 'unit': '500g'}],
            'rice': [{'name': 'SuperValu Basmati Rice 1kg', 'price': 2.26, 'unit': '1kg'}],
            'tomatoes': [{'name': 'SuperValu Cherry Tomatoes 250g', 'price': 2.05, 'unit': '250g'}],
            'onions': [{'name': 'SuperValu White Onions 1kg', 'price': 1.31, 'unit': '1kg'}],
            'potatoes': [{'name': 'SuperValu Rooster Potatoes 2kg', 'price': 2.61, 'unit': '2kg'}],
            'carrots': [{'name': 'SuperValu Carrots 1kg', 'price': 0.93, 'unit': '1kg'}],
            'beef': [{'name': 'SuperValu Beef Mince 500g', 'price': 4.73, 'unit': '500g'}],
            'pork': [{'name': 'SuperValu Pork Chops 500g', 'price': 3.94, 'unit': '500g'}],
            'fish': [{'name': 'SuperValu Salmon Fillet 200g', 'price': 4.19, 'unit': '200g'}],
            'cereal': [{'name': 'SuperValu Cornflakes 500g', 'price': 2.36, 'unit': '500g'}],
            'coffee': [{'name': 'SuperValu Instant Coffee 200g', 'price': 4.73, 'unit': '200g'}],
            'tea': [{'name': 'SuperValu Tea Bags 80pk', 'price': 2.89, 'unit': '80 pack'}],
            'sugar': [{'name': 'SuperValu Granulated Sugar 1kg', 'price': 1.21, 'unit': '1kg'}],
            'flour': [{'name': 'SuperValu Plain Flour 1.5kg', 'price': 1.42, 'unit': '1.5kg'}],
            'oil': [{'name': 'SuperValu Sunflower Oil 1L', 'price': 1.98, 'unit': '1L'}],
            'orange': [{'name': 'SuperValu Oranges 1kg', 'price': 2.09, 'unit': '1kg'}],
            'lemon': [{'name': 'SuperValu Lemons 500g', 'price': 1.31, 'unit': '500g'}],
            'cucumber': [{'name': 'SuperValu Cucumber Each', 'price': 0.79, 'unit': 'each'}],
            'lettuce': [{'name': 'SuperValu Iceberg Lettuce', 'price': 0.93, 'unit': 'each'}]
        }
        
        products = base_products.get(query.lower())
        if not products:
            base_price = random.uniform(1.0, 5.0) * 1.05  # 5% higher than Tesco
            products = [
                {'name': f'SuperValu {query.title()}', 'price': round(base_price, 2), 'unit': 'each'},
                {'name': f'SuperValu Premium {query.title()}', 'price': round(base_price * 1.3, 2), 'unit': 'each'}
            ][:random.randint(1, 2)]
        
        return [self._standardize_product({
            **product,
            'url': self._get_store_url('SuperValu'),
            'image': f'{self.base_url}/images/products/placeholder.jpg'
        }) for product in products]
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class AldiScraper(BaseScraper):
    def __init__(self):
        super().__init__('Aldi', delay=2.0)
        self.base_url = 'https://www.aldi.ie'
    
    def search_products(self, query: str):
        """Search Aldi for products"""
        logger.info(f"Searching Aldi for: {query}")
        return self._get_mock_products(query)
    
    def _get_mock_products(self, query: str):
        """Generate realistic mock data for Aldi"""
        mock_data = {
            'milk': [
                {'name': 'Aldi Fresh Milk 1L', 'price': 1.03, 'unit': '1L'},
                {'name': 'Aldi Fresh Milk 2L', 'price': 1.75, 'unit': '2L'},
                {'name': 'Aldi Organic Milk 1L', 'price': 1.59, 'unit': '1L'},
                {'name': 'Aldi Skimmed Milk 1L', 'price': 1.03, 'unit': '1L'},
                {'name': 'Aldi Whole Milk 500ml', 'price': 0.62, 'unit': '500ml'},
                {'name': 'Aldi Lactose Free Milk 1L', 'price': 1.65, 'unit': '1L'}
            ],
            'bread': [
                {'name': 'Aldi White Bread', 'price': 0.90, 'unit': '800g'},
                {'name': 'Aldi Wholemeal Bread', 'price': 1.09, 'unit': '800g'}
            ],
            'eggs': [
                {'name': 'Aldi Free Range Eggs 12pk', 'price': 2.89, 'unit': '12 pack'}
            ]
        }
        
        products = mock_data.get(query.lower(), [
            {'name': f'Aldi {query.title()}', 'price': 2.05, 'unit': 'each'}
        ])
        
        return [self._standardize_product({
            **product,
            'url': f'{self.base_url}/groceries/{product["name"].lower().replace(" ", "-")}',
            'image': f'{self.base_url}/content/products/placeholder.jpg'
        }) for product in products]
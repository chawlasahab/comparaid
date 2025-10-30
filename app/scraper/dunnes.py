from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class DunnesScraper(BaseScraper):
    def __init__(self):
        super().__init__('Dunnes', delay=2.0)
        self.base_url = 'https://www.dunnesstores.com'
    
    def search_products(self, query: str):
        """Search Dunnes for products"""
        logger.info(f"Searching Dunnes for: {query}")
        return self._get_mock_products(query)
    
    def _get_mock_products(self, query: str):
        """Generate realistic mock data for Dunnes"""
        mock_data = {
            'milk': [
                {'name': 'Dunnes Fresh Milk 1L', 'price': 1.19, 'unit': '1L'},
                {'name': 'Dunnes Fresh Milk 2L', 'price': 2.04, 'unit': '2L'},
                {'name': 'Dunnes Organic Milk 1L', 'price': 1.79, 'unit': '1L'},
                {'name': 'Dunnes Skimmed Milk 1L', 'price': 1.19, 'unit': '1L'},
                {'name': 'Dunnes Whole Milk 500ml', 'price': 0.71, 'unit': '500ml'},
                {'name': 'Dunnes Lactose Free Milk 1L', 'price': 1.85, 'unit': '1L'}
            ],
            'bread': [
                {'name': 'Dunnes White Sliced Pan', 'price': 1.05, 'unit': '800g'},
                {'name': 'Dunnes Wholemeal Bread', 'price': 1.25, 'unit': '800g'}
            ],
            'eggs': [
                {'name': 'Dunnes Free Range Eggs 12pk', 'price': 3.15, 'unit': '12 pack'}
            ]
        }
        
        products = mock_data.get(query.lower(), [
            {'name': f'Dunnes {query.title()}', 'price': 2.35, 'unit': 'each'}
        ])
        
        return [self._standardize_product({
            **product,
            'url': 'https://www.dunnesstoresgrocery.com/sm/delivery/rsid/258/results?q=' + product['name'].replace(' ', '+'),
            'image': f'{self.base_url}/assets/products/placeholder.jpg'
        }) for product in products]
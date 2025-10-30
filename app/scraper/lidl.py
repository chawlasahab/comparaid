from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class LidlScraper(BaseScraper):
    def __init__(self):
        super().__init__('Lidl', delay=2.0)
        self.base_url = 'https://www.lidl.ie'
    
    def search_products(self, query: str):
        """Search Lidl for products"""
        logger.info(f"Searching Lidl for: {query}")
        return self._get_mock_products(query)
    
    def _get_mock_products(self, query: str):
        """Generate realistic mock data for Lidl"""
        mock_data = {
            'milk': [
                {'name': 'Lidl Fresh Milk 1L', 'price': 1.07, 'unit': '1L'},
                {'name': 'Lidl Fresh Milk 2L', 'price': 1.82, 'unit': '2L'},
                {'name': 'Lidl Organic Milk 1L', 'price': 1.65, 'unit': '1L'},
                {'name': 'Lidl Skimmed Milk 1L', 'price': 1.07, 'unit': '1L'},
                {'name': 'Lidl Whole Milk 500ml', 'price': 0.64, 'unit': '500ml'},
                {'name': 'Lidl Lactose Free Milk 1L', 'price': 1.71, 'unit': '1L'}
            ],
            'bread': [
                {'name': 'Lidl White Bread', 'price': 0.94, 'unit': '800g'},
                {'name': 'Lidl Wholemeal Bread', 'price': 1.15, 'unit': '800g'}
            ],
            'eggs': [
                {'name': 'Lidl Free Range Eggs 12pk', 'price': 2.95, 'unit': '12 pack'}
            ]
        }
        
        products = mock_data.get(query.lower(), [
            {'name': f'Lidl {query.title()}', 'price': 2.15, 'unit': 'each'}
        ])
        
        return [self._standardize_product({
            **product,
            'url': f'{self.base_url}/products/{product["name"].lower().replace(" ", "-")}',
            'image': f'{self.base_url}/media/products/placeholder.jpg'
        }) for product in products]
import requests
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, store_name: str, delay: float = 1.0):
        self.store_name = store_name
        self.delay = delay
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Disable SSL verification for development (not recommended for production)
        self.session.verify = False
    
    @abstractmethod
    def search_products(self, query: str) -> List[Dict]:
        """Search for products and return standardized data"""
        pass
    
    def _make_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with error handling and rate limiting"""
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed for {self.store_name}: {e}")
            return None
    
    def _standardize_product(self, raw_data: Dict) -> Dict:
        """Convert raw scraper data to standard format"""
        return {
            'store': self.store_name,
            'product': raw_data.get('name', '').strip(),
            'price': float(raw_data.get('price', 0)),
            'unit': raw_data.get('unit', '').strip(),
            'url': raw_data.get('url', ''),
            'image': raw_data.get('image', '')
        }
    
    def _extract_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        import re
        if not price_text:
            return 0.0
        
        # Remove currency symbols and extract number
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            return float(price_match.group())
        return 0.0
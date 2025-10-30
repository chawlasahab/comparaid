from flask import jsonify, request
from app.api import api_bp
from app.models import Product, Store
from app import limiter
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/prices')
@limiter.limit("30 per minute")
def get_prices():
    """Get product prices with optional search query"""
    query = request.args.get('product', '').strip()
    limit = min(int(request.args.get('limit', 50)), 100)
    
    if not query:
        return jsonify({'error': 'Product query required'}), 400
    
    try:
        products = Product.search_products(query, limit=limit)
        results = [product.to_dict() for product in products]
        
        return jsonify({
            'products': results,
            'count': len(results),
            'query': query
        })
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        return jsonify({'error': 'Search failed'}), 500

@api_bp.route('/stores')
@limiter.limit("10 per minute")
def get_stores():
    """Get list of active stores"""
    try:
        stores = Store.get_active_stores()
        return jsonify({
            'stores': [store.to_dict() for store in stores]
        })
    except Exception as e:
        logger.error(f"Error fetching stores: {e}")
        return jsonify({'error': 'Failed to fetch stores'}), 500

@api_bp.route('/trending')
@limiter.limit("10 per minute")
def get_trending():
    """Get trending/recently updated products"""
    limit = min(int(request.args.get('limit', 10)), 20)
    
    try:
        products = Product.get_trending(limit=limit)
        return jsonify({
            'products': [product.to_dict() for product in products],
            'count': len(products)
        })
    except Exception as e:
        logger.error(f"Error fetching trending products: {e}")
        return jsonify({'error': 'Failed to fetch trending products'}), 500

@api_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ComparAid API'
    })
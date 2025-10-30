from flask import jsonify, request
from app.api import api_bp
from app.models import Product, Store
from app import limiter, db
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/categories')
@limiter.limit("10 per minute")
def get_categories():
    """Get all available product categories"""
    try:
        categories = db.session.query(Product.category, db.func.count(Product.id)).filter(
            Product.is_active == True,
            Product.category.isnot(None)
        ).group_by(Product.category).all()
        
        return jsonify({
            'categories': [{'name': cat, 'count': count} for cat, count in categories]
        })
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({'error': 'Failed to fetch categories'}), 500

@api_bp.route('/products/category/<category>')
@limiter.limit("20 per minute")
def get_products_by_category(category):
    """Get all products in a specific category"""
    limit = min(int(request.args.get('limit', 100)), 500)
    
    try:
        products = Product.query.filter(
            Product.category == category,
            Product.is_active == True
        ).order_by(Product.price.asc()).limit(limit).all()
        
        return jsonify({
            'category': category,
            'products': [product.to_dict() for product in products],
            'count': len(products)
        })
    except Exception as e:
        logger.error(f"Error fetching products for category {category}: {e}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@api_bp.route('/products/brand/<brand>')
@limiter.limit("20 per minute")
def get_products_by_brand(brand):
    """Get all products from a specific brand"""
    limit = min(int(request.args.get('limit', 100)), 500)
    
    try:
        products = Product.query.filter(
            Product.brand.ilike(f'%{brand}%'),
            Product.is_active == True
        ).order_by(Product.price.asc()).limit(limit).all()
        
        return jsonify({
            'brand': brand,
            'products': [product.to_dict() for product in products],
            'count': len(products)
        })
    except Exception as e:
        logger.error(f"Error fetching products for brand {brand}: {e}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@api_bp.route('/products/promotions')
@limiter.limit("10 per minute")
def get_promotional_products():
    """Get all products currently on promotion"""
    limit = min(int(request.args.get('limit', 50)), 200)
    
    try:
        products = Product.query.filter(
            Product.promotion.isnot(None),
            Product.is_active == True
        ).order_by(Product.price.asc()).limit(limit).all()
        
        return jsonify({
            'promotions': [product.to_dict() for product in products],
            'count': len(products)
        })
    except Exception as e:
        logger.error(f"Error fetching promotional products: {e}")
        return jsonify({'error': 'Failed to fetch promotions'}), 500

@api_bp.route('/stats')
@limiter.limit("5 per minute")
def get_database_stats():
    """Get comprehensive database statistics"""
    try:
        total_products = Product.query.filter_by(is_active=True).count()
        total_stores = Store.query.filter_by(is_active=True).count()
        
        # Categories stats
        categories = db.session.query(
            Product.category, 
            db.func.count(Product.id),
            db.func.min(Product.price),
            db.func.max(Product.price),
            db.func.avg(Product.price)
        ).filter(
            Product.is_active == True,
            Product.category.isnot(None)
        ).group_by(Product.category).all()
        
        category_stats = []
        for cat, count, min_price, max_price, avg_price in categories:
            category_stats.append({
                'category': cat,
                'product_count': count,
                'price_range': {
                    'min': float(min_price) if min_price else 0,
                    'max': float(max_price) if max_price else 0,
                    'avg': round(float(avg_price), 2) if avg_price else 0
                }
            })
        
        return jsonify({
            'total_products': total_products,
            'total_stores': total_stores,
            'categories': category_stats,
            'last_updated': Product.query.filter_by(is_active=True).order_by(Product.last_updated.desc()).first().last_updated.isoformat() if total_products > 0 else None
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500
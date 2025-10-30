from flask import render_template, request, jsonify
from app.main import main_bp
from app.models import Product, Store
from app import limiter
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('home.html')

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/stores')
def stores():
    """Stores page with details"""
    stores = Store.query.all()
    store_stats = []
    for store in stores:
        product_count = Product.query.filter_by(store_id=store.id, is_active=True).count()
        avg_price = Product.query.filter_by(store_id=store.id, is_active=True).with_entities(func.avg(Product.price)).scalar() or 0
        store_stats.append({
            'store': store,
            'product_count': product_count,
            'avg_price': round(avg_price, 2)
        })
    return render_template('stores.html', store_stats=store_stats)

@main_bp.route('/categories')
def categories():
    """Categories page"""
    categories = [
        {'name': 'Dairy & Eggs', 'items': ['milk', 'eggs', 'butter', 'cheese', 'yogurt'], 'icon': '🥛'},
        {'name': 'Meat & Fish', 'items': ['chicken', 'beef', 'pork', 'fish', 'bacon'], 'icon': '🥩'},
        {'name': 'Fruits & Vegetables', 'items': ['apples', 'bananas', 'oranges', 'potatoes', 'carrots'], 'icon': '🍎'},
        {'name': 'Pantry Staples', 'items': ['bread', 'pasta', 'rice', 'flour', 'sugar'], 'icon': '🍞'},
        {'name': 'Beverages', 'items': ['coffee', 'tea', 'juice', 'water', 'wine'], 'icon': '☕'},
        {'name': 'Household', 'items': ['soap', 'shampoo', 'toothpaste', 'detergent', 'tissues'], 'icon': '🧽'}
    ]
    return render_template('categories.html', categories=categories)

@main_bp.route('/trends')
def trends():
    """Price trends page"""
    popular_items = ['milk', 'bread', 'eggs', 'butter', 'chicken']
    trends_data = []
    for item in popular_items:
        products = Product.query.filter(Product.search_term.ilike(f'%{item}%'), Product.is_active == True).all()
        if products:
            prices = [p.price for p in products]
            trends_data.append({
                'item': item.title(),
                'min_price': min(prices),
                'max_price': max(prices),
                'avg_price': round(sum(prices) / len(prices), 2),
                'stores': len(set(p.store.name for p in products))
            })
    return render_template('trends.html', trends_data=trends_data)

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@main_bp.route('/search')
@limiter.limit("20 per minute")
def search():
    """Search products and return JSON"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Please enter a search term'})
    
    try:
        products = Product.search_products(query, limit=50)
        results = [product.to_dict() for product in products]
        results.sort(key=lambda x: x['price'])
        
        return jsonify({
            'products': results,
            'cached': True,
            'last_updated': products[0].last_updated.isoformat() if products else None
        })
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': 'Search failed. Please try again.'})
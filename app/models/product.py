from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    store_url = db.Column(db.String(500))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    search_term = db.Column(db.String(100), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    store = db.relationship('Store', backref='products')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'store': self.store.name,
            'price': self.price,
            'unit': self.unit or 'each',
            'image_url': self.image_url,
            'store_url': self.store_url,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def search_products(cls, query, limit=50):
        return cls.query.filter(
            cls.search_term.ilike(f'%{query}%'),
            cls.is_active == True
        ).order_by(cls.price.asc()).limit(limit).all()
    
    @classmethod
    def get_trending(cls, limit=10):
        return cls.query.filter(
            cls.is_active == True
        ).order_by(cls.last_updated.desc()).limit(limit).all()
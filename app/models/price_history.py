from app import db
from datetime import datetime

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    product = db.relationship('Product', backref='price_history')
    
    @classmethod
    def record_price(cls, product_id, price):
        history = cls(product_id=product_id, price=price)
        db.session.add(history)
        return history
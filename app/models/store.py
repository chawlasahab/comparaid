from app import db

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    website = db.Column(db.String(200))
    logo_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    scraper_enabled = db.Column(db.Boolean, default=True)
    last_scraped = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'logo_url': self.logo_url,
            'is_active': self.is_active
        }
    
    @classmethod
    def get_active_stores(cls):
        return cls.query.filter(cls.is_active == True).all()
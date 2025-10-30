from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///grocery_prices.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.api import api_bp
    from app.main import main_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)
    
    return app
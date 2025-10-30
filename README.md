# ComparAid

Irish grocery price comparison platform that helps you find the best deals across major supermarkets.

## Features

- **Multi-Store Comparison**: Compare prices across Tesco, SuperValu, Dunnes, Lidl, and Aldi
- **Real-Time Search**: Instant price comparison with comprehensive product database
- **Category Browsing**: Browse products by categories (Dairy, Meat, Vegetables, etc.)
- **Responsive Design**: Mobile-first design with professional Irish-themed styling
- **Rate Limited API**: Production-ready with request limiting and caching
- **Legal Compliance**: Respectful scraping with 2-day intervals

## Tech Stack

- **Backend**: Flask, SQLAlchemy, APScheduler
- **Database**: SQLite (development), PostgreSQL (production)
- **Caching**: Redis
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker, Gunicorn, Docker Compose

## Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/chawlasahab/comparaid.git
cd comparaid

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Run application
python main.py
```

Visit `http://localhost:8765`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual container
docker build -t comparaid .
docker run -p 5000:5000 comparaid
```

## Configuration

Key environment variables:

```env
DATABASE_URL=sqlite:///grocery_prices.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
SCRAPING_DELAY=2.0
```

## API Endpoints

- `GET /` - Home page with search
- `GET /api/search?q=milk` - Search products
- `GET /categories` - Browse by category
- `GET /stores` - Store information
- `GET /api/health` - Health check

## Architecture

```
├── app/
│   ├── api/          # API routes
│   ├── main/         # Web routes
│   ├── models/       # Database models
│   ├── scraper/      # Store scrapers
│   ├── static/       # CSS, JS, images
│   └── templates/    # HTML templates
├── instance/         # Database files
└── docker-compose.yml
```

## Legal Notice

This application respects robots.txt and implements rate limiting. Scraping is performed with 2-day intervals and appropriate delays between requests.

## License

MIT License - see LICENSE file for details.
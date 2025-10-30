// ComparAid - Modern JavaScript

class ComparAid {
    constructor() {
        this.searchForm = document.getElementById('searchForm');
        this.searchInput = document.getElementById('searchInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        this.resultsGrid = document.getElementById('resultsGrid');
        this.resultsTitle = document.getElementById('resultsTitle');
        this.lastUpdated = document.getElementById('lastUpdated');
        this.errorMessage = document.getElementById('errorMessage');
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.searchInput.focus();
        this.setupStickyHeader();
    }

    bindEvents() {
        this.searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = this.searchInput.value.trim();
            if (query) {
                this.searchProducts(query);
            }
        });

        document.querySelectorAll('.popular-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const term = tag.getAttribute('data-term');
                this.searchInput.value = term;
                this.searchProducts(term);
            });
        });

        // Smooth scroll to results
        window.addEventListener('scroll', this.handleScroll.bind(this));
    }

    setupStickyHeader() {
        const header = document.getElementById('header');
        let lastScrollY = window.scrollY;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            } else {
                header.style.boxShadow = 'none';
            }
        });
    }

    async searchProducts(query) {
        this.showLoading();
        this.hideResults();
        this.hideError();
        this.scrollToSection(this.loadingSection);

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            this.hideLoading();

            if (data.error) {
                this.showError(data.error);
            } else if (data.products && data.products.length > 0) {
                this.displayResults(data.products, data.cached, data.last_updated, query);
                this.scrollToSection(this.resultsSection);
            } else {
                this.showError(`No products found for "${query}". Try searching for milk, bread, eggs, or other common groceries.`);
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Unable to fetch prices right now. Please check your connection and try again.');
            console.error('Search error:', error);
        }
    }

    displayResults(products, cached, lastUpdatedTime, query) {
        const cheapestPrice = Math.min(...products.map(p => p.price));
        
        this.resultsTitle.textContent = `Results for "${query}" (${products.length} found)`;
        
        const cacheStatus = cached ? 'cached' : 'fresh';
        this.lastUpdated.innerHTML = `
            <span>Last updated: ${this.formatDateTime(lastUpdatedTime)}</span>
            <span style="margin-left: 8px; color: ${cached ? '#d97706' : '#059669'};">
                ${cached ? '📋 Cached' : '🔄 Fresh'}
            </span>
        `;

        this.resultsGrid.innerHTML = products.map(product => {
            const isCheapest = product.price === cheapestPrice;
            return this.createProductCard(product, isCheapest);
        }).join('');

        // Animate cards in
        this.animateCards();
        this.showResults();
    }

    createProductCard(product, isCheapest) {
        return `
            <div class="product-card ${isCheapest ? 'cheapest' : ''}" style="opacity: 0; transform: translateY(20px);">
                <div class="product-header">
                    <div>
                        <h3 class="product-name">${product.name}</h3>
                        <p class="product-unit">${product.unit || 'each'}</p>
                    </div>
                    <span class="store-badge ${product.store.toLowerCase()}">${product.store}</span>
                </div>
                <div class="product-footer">
                    <div class="price-container">
                        <span class="price">€${product.price.toFixed(2)}</span>
                        ${isCheapest ? '<span class="cheapest-badge">🏆 Best Price</span>' : ''}
                    </div>
                    <a href="${product.store_url}" target="_blank" class="store-link">
                        View Store
                    </a>
                </div>
            </div>
        `;
    }

    animateCards() {
        const cards = this.resultsGrid.querySelectorAll('.product-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.style.transition = 'all 0.4s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    showLoading() {
        this.loadingSection.style.display = 'block';
        this.searchBtn.disabled = true;
        this.searchBtn.innerHTML = `
            <span class="search-text">Searching...</span>
            <div style="width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top: 2px solid white; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        `;
    }

    hideLoading() {
        this.loadingSection.style.display = 'none';
        this.searchBtn.disabled = false;
        this.searchBtn.innerHTML = `
            <span class="search-text">Compare Prices</span>

        `;
    }

    showResults() {
        this.resultsSection.style.display = 'block';
        this.resultsSection.style.opacity = '0';
        setTimeout(() => {
            this.resultsSection.style.transition = 'opacity 0.3s ease-in';
            this.resultsSection.style.opacity = '1';
        }, 100);
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorSection.style.display = 'block';
        this.scrollToSection(this.errorSection);
    }

    hideError() {
        this.errorSection.style.display = 'none';
    }

    scrollToSection(section) {
        setTimeout(() => {
            section.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        
        return date.toLocaleDateString('en-IE', {
            day: 'numeric',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    handleScroll() {
        // Add any scroll-based animations here
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ComparAid();
});

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.classList.toggle('active');
}
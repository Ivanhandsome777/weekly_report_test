// Industry Weekly Reports - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Add smooth scrolling for anchor links
    addSmoothScrolling();
    
    // Add loading animations
    addLoadingAnimations();
    
    // Add interactive features
    addInteractiveFeatures();
    
    // Initialize API features
    initializeAPI();
}

function addSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addLoadingAnimations() {
    // Add fade-in animation to cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.report-card, .feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

function addInteractiveFeatures() {
    // Add hover effects to report cards
    document.querySelectorAll('.report-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click tracking for analytics
    document.querySelectorAll('.report-card').forEach(card => {
        card.addEventListener('click', function() {
            const reportTitle = this.querySelector('.report-title').textContent;
            console.log(`Report clicked: ${reportTitle}`);
            
            // You can add analytics tracking here
            // gtag('event', 'report_view', { report_name: reportTitle });
        });
    });
}

function initializeAPI() {
    // Add API testing functionality
    const apiSection = document.querySelector('.api-section');
    if (apiSection) {
        addAPITester();
    }
}

function addAPITester() {
    // Create API tester button
    const testButton = document.createElement('button');
    testButton.textContent = 'Test API';
    testButton.className = 'btn btn-primary';
    testButton.style.marginTop = '1rem';
    
    testButton.addEventListener('click', async function() {
        try {
            this.textContent = 'Testing...';
            this.disabled = true;
            
            const response = await fetch('/api/reports');
            const data = await response.json();
            
            // Show results
            showAPIResults(data);
            
            this.textContent = 'Test API';
            this.disabled = false;
        } catch (error) {
            console.error('API test failed:', error);
            showAPIError(error.message);
            
            this.textContent = 'Test API';
            this.disabled = false;
        }
    });
    
    document.querySelector('.api-section').appendChild(testButton);
}

function showAPIResults(data) {
    // Create or update results display
    let resultsDiv = document.querySelector('.api-results');
    if (!resultsDiv) {
        resultsDiv = document.createElement('div');
        resultsDiv.className = 'api-results';
        document.querySelector('.api-section').appendChild(resultsDiv);
    }
    
    resultsDiv.innerHTML = `
        <h4>API Response:</h4>
        <pre><code>${JSON.stringify(data, null, 2)}</code></pre>
    `;
    
    // Add styling
    resultsDiv.style.marginTop = '1rem';
    resultsDiv.style.padding = '1rem';
    resultsDiv.style.background = '#f8f9fa';
    resultsDiv.style.borderRadius = '0.5rem';
    resultsDiv.style.border = '1px solid #e9ecef';
    
    const code = resultsDiv.querySelector('code');
    code.style.fontSize = '0.875rem';
    code.style.color = '#2c3e50';
}

function showAPIError(message) {
    let resultsDiv = document.querySelector('.api-results');
    if (!resultsDiv) {
        resultsDiv = document.createElement('div');
        resultsDiv.className = 'api-results';
        document.querySelector('.api-section').appendChild(resultsDiv);
    }
    
    resultsDiv.innerHTML = `
        <h4>API Error:</h4>
        <p style="color: #e74c3c;">${message}</p>
    `;
    
    resultsDiv.style.marginTop = '1rem';
    resultsDiv.style.padding = '1rem';
    resultsDiv.style.background = '#fff5f5';
    resultsDiv.style.borderRadius = '0.5rem';
    resultsDiv.style.border = '1px solid #fed7d7';
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeApp,
        addSmoothScrolling,
        addLoadingAnimations,
        addInteractiveFeatures,
        debounce,
        throttle
    };
}


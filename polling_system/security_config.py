"""
Security configuration and utilities for the polling system.
"""
import os
from datetime import timedelta
from django.conf import settings

# Security constants
MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT_MINUTES = 15
TOKEN_EXPIRY_HOURS = 24
MAX_POLLS_PER_USER = 50
MAX_VOTES_PER_USER_PER_POLL = 1

# Rate limiting settings
RATE_LIMITS = {
    'auth': {
        'login': '5/minute',
        'register': '3/hour',
        'token': '10/minute',
    },
    'polls': {
        'create': '10/hour',
        'vote': '100/hour',
        'list': '1000/hour',
    }
}

# Input validation patterns
VALIDATION_PATTERNS = {
    'username': r'^[a-zA-Z0-9_]{3,30}$',
    'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'poll_question': r'^[^<>"\']{5,200}$',
    'option_text': r'^[^<>"\']{1,100}$',
}

# Security headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}

def get_security_settings():
    """Get security settings based on environment."""
    is_production = not settings.DEBUG
    
    return {
        'DEBUG': settings.DEBUG,
        'SECURE_SSL_REDIRECT': is_production,
        'SESSION_COOKIE_SECURE': is_production,
        'CSRF_COOKIE_SECURE': is_production,
        'SECURE_BROWSER_XSS_FILTER': True,
        'SECURE_CONTENT_TYPE_NOSNIFF': True,
        'X_FRAME_OPTIONS': 'DENY',
        'SECURE_HSTS_SECONDS': 31536000 if is_production else 0,
        'SECURE_HSTS_INCLUDE_SUBDOMAINS': is_production,
        'SECURE_HSTS_PRELOAD': is_production,
    }

def validate_environment():
    """Validate that required environment variables are set in production."""
    if not settings.DEBUG:
        required_vars = [
            'SECRET_KEY',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True 
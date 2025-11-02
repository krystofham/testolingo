import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': os.environ.get('DB_USER', 'main_user'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'testolingo')
}

# Application configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'vygeneruj-silny-tajny-klic')  # Pro produkci změň!
import os

class Config:
    """Base configuration."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
    DEBUG = False
    TESTING = False
    HOST = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_RUN_PORT', 5000))

    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../data', 'database.db')}"
    DEBUG = True


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
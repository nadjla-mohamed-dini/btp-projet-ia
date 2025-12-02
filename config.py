import os
from datetime import timedelta


class Config:
    """Configuration de base"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    
    # If DB env vars are present, try to use Postgres. Otherwise, use a local SQLite DB for dev.
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT') or 5432
    DB_NAME = os.environ.get('DB_NAME') or 'Feelflix'

    if all([DB_USER, DB_PASSWORD, DB_HOST]):
        SQLALCHEMY_DATABASE_URI = (
            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )
    else:
        # fallback to sqlite file to allow local dev without Postgres/psycopg2 installed
        SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False
    
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT') or 5432
    DB_NAME = 'Feelflix'
    
    # NOTE: don't raise here at import time — perform validation in `get_config`
    
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


def get_config(env=None):
    """Retourne la configuration appropriée selon l'environnement"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    # If production selected, ensure required DB env vars are present
    if env == 'production':
        prod_cfg = config_map.get('production')
        # read required values from environment
        DB_USER = os.environ.get('DB_USER')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_HOST = os.environ.get('DB_HOST')
        if not all([DB_USER, DB_PASSWORD, DB_HOST]):
            raise ValueError("Variables d'environnement DB_USER, DB_PASSWORD et DB_HOST requises pour l'environnement de production")

    return config_map.get(env, DevelopmentConfig)

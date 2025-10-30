# -*- coding: utf-8 -*-
import os

class Config:
    """Configuration de base"""
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "Feelflix")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False

    def __init__(self):
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "Feelflix")

        if not all([db_user, db_password, db_host]):
            raise ValueError("Variables d'environnement DB_USER, DB_PASSWORD et DB_HOST requises")

        self.SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Configuration pour les tests"""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config(env=None):
    """Retourne la configuration appropriée selon l'environnement"""
    if env is None:
        env = os.getenv("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_class = config_map.get(env, DevelopmentConfig)

    # Si la classe a un constructeur personnalisé, on l’instancie
    return config_class() if callable(config_class) else config_class


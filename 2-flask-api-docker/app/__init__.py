"""
Flask API — Application Factory
Production-grade REST API with JWT auth, rate limiting, and structured logging.

Author: Gaurav Kumar
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name: str = None) -> Flask:
    """
    Application factory pattern — creates and configures the Flask app.
    Enables easy testing with different configs.
    """
    app = Flask(__name__)

    # Load config based on environment
    env = config_name or os.getenv("FLASK_ENV", "development")
    config_map = {
        "development": "app.config.DevelopmentConfig",
        "production": "app.config.ProductionConfig",
        "testing": "app.config.TestingConfig",
    }
    app.config.from_object(config_map.get(env, config_map["development"]))

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Structured JSON logging
    _configure_logging(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.items import items_bp
    from app.routes.health import health_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(items_bp, url_prefix="/api/items")
    app.register_blueprint(health_bp, url_prefix="/api")

    # Create tables on startup
    with app.app_context():
        db.create_all()

    return app


def _configure_logging(app: Flask):
    """Configure structured logging for CloudWatch ingestion."""
    log_level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}',
    )
    app.logger.setLevel(log_level)

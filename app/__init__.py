"""
Flask Application Factory

This module implements the Flask application factory pattern, which allows
creating multiple application instances with different configurations.
This is essential for testing and deployment flexibility.
"""

from flask import Flask
from config import Config
from app.db import init_db


def create_app(config_class=Config):
    """
    Create and configure a Flask application instance.
    
    This function implements the Application Factory pattern, allowing
    different configurations to be used for development, testing, and production.
    
    Args:
        config_class (class, optional): Configuration class to use.
                                       Defaults to Config for development.
    
    Returns:
        Flask: Configured Flask application instance
        
    Example:
        # Development app
        app = create_app()
        
        # Test app with different database
        app = create_app(TestConfig)
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration from the specified config class
    app.config.from_object(config_class)
    
    # Initialize database with this app instance
    # This binds SQLAlchemy to the Flask app
    init_db(app)
    
    # Setup routes using Flask decorators
    # This is simpler than both Blueprints and manual registration
    from app.routes import setup_routes
    setup_routes(app)
    
    return app
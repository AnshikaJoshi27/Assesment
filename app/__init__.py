"""
Flask Application Factory

This module implements the Flask application factory pattern, which allows
creating multiple application instances with different configurations.
This is essential for testing and deployment flexibility.
"""

from flask import Flask, jsonify
from config import Config
from app.db import init_db
import logging
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


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
    from app.routes import setup_routes
    setup_routes(app)
    
    # Register error handlers for proper exception handling
    register_error_handlers(app)
    
    # Setup logging for production debugging
    setup_logging(app)
    
    return app


def register_error_handlers(app):
    """
    Register comprehensive error handlers for the Flask application.
    
    This function sets up handlers for common HTTP errors, database errors,
    validation errors, and unexpected exceptions to provide consistent
    JSON error responses.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle bad request errors (400)"""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request was malformed or invalid',
            'status_code': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle not found errors (404)"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(405) 
    def method_not_allowed_error(error):
        """Handle method not allowed errors (405)"""
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The HTTP method is not allowed for this endpoint',
            'status_code': 405
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors (500)"""
        # Log the actual error for debugging
        app.logger.error(f'Internal server error: {str(error)}')
        
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred on the server',
            'status_code': 500
        }), 500
    
    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        """Handle database-related errors"""
        # Log database error details
        app.logger.error(f'Database error: {str(error)}')
        
        # Rollback any pending database transaction
        from app.db import db
        db.session.rollback()
        
        return jsonify({
            'error': 'Database Error',
            'message': 'A database error occurred. Please try again',
            'status_code': 500
        }), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        """Handle Marshmallow validation errors"""
        return jsonify({
            'error': 'Validation Error', 
            'message': 'Input data validation failed',
            'details': error.messages,
            'status_code': 400
        }), 400
    
    @app.errorhandler(ValueError)
    def value_error(error):
        """Handle value errors (invalid input data)"""
        return jsonify({
            'error': 'Invalid Value',
            'message': str(error),
            'status_code': 400
        }), 400
    
    @app.errorhandler(KeyError)
    def key_error(error):
        """Handle missing required fields"""
        return jsonify({
            'error': 'Missing Field',
            'message': f'Required field missing: {str(error)}',
            'status_code': 400
        }), 400
    
    @app.errorhandler(Exception)
    def general_exception_handler(error):
        """Handle any unhandled exceptions"""
        # Log the full exception details
        app.logger.error(f'Unhandled exception: {str(error)}', exc_info=True)
        
        # Don't expose internal error details in production
        if app.config.get('DEBUG'):
            return jsonify({
                'error': 'Unhandled Exception',
                'message': str(error),
                'type': type(error).__name__,
                'status_code': 500
            }), 500
        else:
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'status_code': 500
            }), 500


def setup_logging(app):
    """
    Setup application logging for debugging and monitoring.
    
    Configures different log levels for development and production
    environments to help with debugging and error tracking.
    
    Args:
        app (Flask): Flask application instance
    """
    if not app.debug and not app.testing:
        # Production logging setup
        if app.config.get('LOG_TO_STDOUT'):
            # Log to stdout for containerized deployments
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            # Log to file for traditional deployments
            file_handler = logging.FileHandler('logs/salary_api.log')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Salary Management API startup')
    else:
        # Development logging - more verbose
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Salary Management API started in debug mode')
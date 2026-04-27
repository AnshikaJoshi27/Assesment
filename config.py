"""
Application Configuration Settings

This module defines configuration classes for different environments:
- Config: Default development configuration
- TestConfig: Configuration for running tests

The configuration uses environment variables where available,
with sensible defaults for development.
"""

import os
from dotenv import load_dotenv

# Get the absolute path to the directory containing this file
# This is used to construct paths relative to the project root
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file if it exists
# This allows configuration through environment files
load_dotenv()


class Config:
    """
    Default configuration for development environment.
    
    Uses environment variables when available, falls back to
    development defaults. This configuration creates a SQLite
    database file in the project root directory.
    """
    
    # Secret key for session management and CSRF protection
    # In production, this MUST be a strong, random secret
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database connection string
    # Default: SQLite database file in project root
    # Override with DATABASE_URL environment variable for production
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        'sqlite:///' + os.path.join(basedir, 'salary_management.db')
    )
    
    # Disable SQLAlchemy track modifications (improves performance)
    # This disables the SQLAlchemy event system for object modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """
    Configuration for testing environment.
    
    Inherits from base Config but overrides database to use
    in-memory SQLite for fast, isolated testing.
    """
    
    # Enable testing mode in Flask
    TESTING = True
    
    # Use in-memory SQLite database for tests
    # This provides fast, isolated testing without file I/O
    # Each test gets a clean database that's automatically cleaned up
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
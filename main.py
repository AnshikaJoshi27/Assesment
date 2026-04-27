#!/usr/bin/env python3
"""
Salary Management API - Application Entry Point

This module serves as the main entry point for the Flask salary management API.
It creates the Flask application instance, initializes the database, seeds sample data,
and starts the development server.

Usage:
    python main.py

The application will:
1. Create database tables if they don't exist
2. Seed sample employee data for testing
3. Start the Flask development server on http://localhost:5000
"""

from app import create_app
from app.db import db, create_tables, seed_sample_data
from app.models import Employee

# Create the Flask application instance using the application factory pattern
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Make database instance and Employee model available in Flask shell.
    
    This allows you to run 'flask shell' and directly use:
    - db: SQLAlchemy database instance
    - Employee: Employee model class
    
    Returns:
        dict: Context variables for Flask shell
    """
    return {'db': db, 'Employee': Employee}


if __name__ == '__main__':
    # Create application context for database operations
    with app.app_context():
        # Initialize database tables
        create_tables()
        
        # Add sample data for development and testing
        seed_sample_data()
    
    # Start the Flask development server
    # Debug mode enables hot reloading and detailed error messages
    app.run(debug=True)
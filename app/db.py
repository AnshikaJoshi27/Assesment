"""
Database Configuration and Utilities

This module centralizes all database-related code including:
- SQLAlchemy instance initialization
- Database setup and teardown utilities
- Sample data seeding functions
- Development and testing helpers

Separating database logic from the main app factory provides better
organization and makes testing easier.
"""

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance without binding to any specific app
# This allows us to use the application factory pattern
db = SQLAlchemy()


def init_db(app):
    """
    Initialize database with Flask app.
    
    This function binds the SQLAlchemy instance to a Flask application.
    Called during app creation in the application factory.
    
    Args:
        app (Flask): Flask application instance to bind database to
    """
    db.init_app(app)


def create_tables():
    """
    Create all database tables.
    
    Creates all tables defined in SQLAlchemy models.
    This is idempotent - won't recreate existing tables.
    
    Note:
        Must be called within Flask application context.
    """
    db.create_all()


def drop_tables():
    """
    Drop all database tables.
    
    WARNING: This will delete all data in the database!
    Primarily used for testing and development.
    
    Note:
        Must be called within Flask application context.
    """
    db.drop_all()


def reset_db():
    """
    Reset database by dropping and recreating all tables.
    
    This provides a clean slate for testing and development.
    WARNING: This will delete all existing data!
    
    Note:
        Must be called within Flask application context.
    """
    drop_tables()    # Remove all existing tables and data
    create_tables()  # Recreate empty tables


def seed_sample_data():
    """
    Add sample employee data for development and testing.
    
    This function populates the database with sample employees
    representing different countries and job titles. Only runs
    if the database is empty (no existing employees).
    
    Sample data includes:
    - Employees from different countries (India, US, Canada)
    - Various job titles (Engineer, Manager, Data Scientist)
    - Different salary ranges for testing tax calculations
    
    Note:
        Must be called within Flask application context.
    """
    # Import here to avoid circular imports
    from app.models import Employee
    
    # Only seed data if database is empty
    if Employee.query.count() == 0:
        # Create sample employees with different countries and salaries
        # This tests various tax calculation scenarios
        employees = [
            Employee(
                full_name="John Doe", 
                job_title="Software Engineer", 
                country="India",           # 10% TDS
                salary=100000
            ),
            Employee(
                full_name="Jane Smith", 
                job_title="Product Manager", 
                country="United States",   # 12% TDS
                salary=120000
            ),
            Employee(
                full_name="Bob Wilson", 
                job_title="Data Scientist", 
                country="Canada",          # No TDS (0%)
                salary=95000
            ),
        ]
        
        # Add all sample employees to the database session
        for emp in employees:
            db.session.add(emp)
        
        # Commit the transaction to save data
        db.session.commit()
        
        print(f"✅ Seeded {len(employees)} sample employees to database")
"""
Test Configuration and Fixtures

This module provides pytest fixtures for testing the salary management API.
Fixtures provide reusable test setup and data for consistent testing.

Key fixtures:
- client: Flask test client with clean database for each test
- sample_employee_data: Standard employee data for testing
"""

import pytest
from app import create_app
from app.db import db, reset_db
from app.models import Employee
from config import TestConfig


@pytest.fixture
def client():
    """
    Create a Flask test client with a clean database for each test.
    
    This fixture:
    1. Creates a Flask app instance using TestConfig (in-memory SQLite)
    2. Provides a test client for making HTTP requests
    3. Sets up a clean database before each test
    4. Cleans up database session after each test
    
    The database is completely isolated for each test, ensuring
    tests don't interfere with each other.
    
    Yields:
        FlaskClient: Test client for making API requests
    """
    # Create app with test configuration (in-memory database)
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    
    # Create test client and application context
    with app.test_client() as client:
        with app.app_context():
            # Reset database to clean state for this test
            reset_db()
            
            # Yield the test client for the test function
            yield client
            
            # Clean up database session after test completes
            db.session.remove()


@pytest.fixture
def sample_employee_data():
    """
    Provide standard employee data for testing.
    
    This fixture returns a dictionary with valid employee data
    that can be used across multiple tests for consistency.
    
    The data includes:
    - Standard Indian employee (10% TDS)
    - Software Engineer role
    - Valid salary amount
    
    Returns:
        dict: Valid employee data for API requests
    """
    return {
        'full_name': 'John Doe',        # Valid name within length limit
        'job_title': 'Software Engineer', # Valid job title
        'country': 'India',             # Country with 10% TDS for testing
        'salary': 100000.0              # Valid positive salary
    }
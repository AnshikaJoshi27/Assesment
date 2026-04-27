"""
Test Exception Handling for Salary Management API

This test module verifies that the Flask application properly handles
various error conditions and returns appropriate error responses.
"""

import pytest
import json
from app import create_app
from app.db import create_tables, reset_db
from config import TestConfig


@pytest.fixture
def test_client():
    """Create a test Flask client with test database"""
    app = create_app(TestConfig)
    
    with app.test_client() as client:
        with app.app_context():
            reset_db()
            create_tables()
            yield client


class TestErrorHandling:
    """Test error handling for various scenarios"""
    
    def test_404_error_for_nonexistent_employee(self, test_client):
        """Test 404 error when requesting nonexistent employee"""
        response = test_client.get('/employees/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Employee Not Found'
        assert 'message' in data
        
    def test_validation_error_for_invalid_employee_data(self, test_client):
        """Test validation error when creating employee with invalid data"""
        invalid_data = {
            "name": "",  # Empty name should fail validation
            "email": "invalid-email",  # Invalid email format
            "salary": -1000  # Negative salary should fail
        }
        
        response = test_client.post('/employees', 
                                  json=invalid_data,
                                  content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Validation Error'
        assert 'details' in data
        
    def test_missing_json_data_error(self, test_client):
        """Test error when creating employee without JSON data"""
        response = test_client.post('/employees', content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing JSON data' in data['message']
        
    def test_country_metrics_for_nonexistent_country(self, test_client):
        """Test 404 error for country with no employees"""
        response = test_client.get('/salary-metrics/country/NonexistentCountry')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'No Data Available'
        assert 'NonexistentCountry' in data['message']
        
    def test_job_title_metrics_for_nonexistent_job(self, test_client):
        """Test 404 error for job title with no employees"""
        response = test_client.get('/salary-metrics/job-title/NonexistentJob')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'No Data Available'
        assert 'NonexistentJob' in data['message']
        
    def test_empty_country_parameter(self, test_client):
        """Test error for empty country parameter"""
        response = test_client.get('/salary-metrics/country/')
        
        # This will hit Flask's routing error (404)
        assert response.status_code == 404
        
    def test_empty_job_title_parameter(self, test_client):
        """Test error for empty job title parameter"""
        response = test_client.get('/salary-metrics/job-title/')
        
        # This will hit Flask's routing error (404)
        assert response.status_code == 404
        
    def test_update_nonexistent_employee(self, test_client):
        """Test error when updating nonexistent employee"""
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        response = test_client.put('/employees/999',
                                 json=update_data,
                                 content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Employee Not Found'
        
    def test_delete_nonexistent_employee(self, test_client):
        """Test error when deleting nonexistent employee"""
        response = test_client.delete('/employees/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Employee Not Found'
        
    def test_salary_calculation_for_nonexistent_employee(self, test_client):
        """Test error when calculating salary for nonexistent employee"""
        response = test_client.get('/employees/999/salary-calculation')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Employee Not Found'
        
    def test_method_not_allowed_error(self, test_client):
        """Test 405 error for unsupported HTTP methods"""
        # Try PATCH on employees endpoint which only supports GET and POST
        response = test_client.patch('/employees')
        
        assert response.status_code == 405
        # The error handler should be triggered (check by looking at content type)
        assert response.content_type == 'application/json'


class TestApplicationErrorHandlers:
    """Test Flask application-level error handlers"""
    
    def test_general_404_error_handler(self, test_client):
        """Test general 404 error handler for nonexistent endpoints"""
        response = test_client.get('/nonexistent-endpoint')
        
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Not Found'
        
    def test_method_not_allowed_error_handler(self, test_client):
        """Test 405 error handler"""
        # Try DELETE on the employees collection endpoint
        response = test_client.delete('/employees')
        
        assert response.status_code == 405
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Method Not Allowed'


if __name__ == '__main__':
    pytest.main([__file__])
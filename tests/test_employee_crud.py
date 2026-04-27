import json
import pytest
from app.models import Employee
from app.db import db


class TestEmployeeCRUD:
    """Test Employee CRUD operations"""
    
    def test_create_employee_success(self, client, sample_employee_data):
        """Test successful employee creation"""
        response = client.post('/employees', 
                             data=json.dumps(sample_employee_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['full_name'] == sample_employee_data['full_name']
        assert data['job_title'] == sample_employee_data['job_title']
        assert data['country'] == sample_employee_data['country']
        assert data['salary'] == sample_employee_data['salary']
        assert 'id' in data
    
    def test_create_employee_validation_errors(self, client):
        """Test employee creation with validation errors"""
        invalid_data = {
            'full_name': '',  # Empty name
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': -1000  # Negative salary
        }
        
        response = client.post('/employees',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
    
    def test_create_employee_missing_fields(self, client):
        """Test employee creation with missing required fields"""
        incomplete_data = {
            'full_name': 'John Doe'
            # Missing required fields
        }
        
        response = client.post('/employees',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_get_all_employees(self, client, sample_employee_data):
        """Test retrieving all employees"""
        # Create an employee first
        client.post('/employees',
                   data=json.dumps(sample_employee_data),
                   content_type='application/json')
        
        response = client.get('/employees')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['full_name'] == sample_employee_data['full_name']
    
    def test_get_employee_by_id(self, client, sample_employee_data):
        """Test retrieving employee by ID"""
        # Create an employee first
        create_response = client.post('/employees',
                                    data=json.dumps(sample_employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        response = client.get(f'/employees/{employee_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == employee_id
        assert data['full_name'] == sample_employee_data['full_name']
    
    def test_get_employee_not_found(self, client):
        """Test retrieving non-existent employee"""
        response = client.get('/employees/999')
        assert response.status_code == 404
    
    def test_update_employee(self, client, sample_employee_data):
        """Test updating employee"""
        # Create an employee first
        create_response = client.post('/employees',
                                    data=json.dumps(sample_employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        # Update the employee
        updated_data = sample_employee_data.copy()
        updated_data['salary'] = 120000.0
        updated_data['job_title'] = 'Senior Software Engineer'
        
        response = client.put(f'/employees/{employee_id}',
                            data=json.dumps(updated_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['salary'] == 120000.0
        assert data['job_title'] == 'Senior Software Engineer'
    
    def test_update_employee_not_found(self, client, sample_employee_data):
        """Test updating non-existent employee"""
        response = client.put('/employees/999',
                            data=json.dumps(sample_employee_data),
                            content_type='application/json')
        assert response.status_code == 404
    
    def test_delete_employee(self, client, sample_employee_data):
        """Test deleting employee"""
        # Create an employee first
        create_response = client.post('/employees',
                                    data=json.dumps(sample_employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        # Delete the employee
        response = client.delete(f'/employees/{employee_id}')
        assert response.status_code == 204
        
        # Verify employee is deleted
        get_response = client.get(f'/employees/{employee_id}')
        assert get_response.status_code == 404
    
    def test_delete_employee_not_found(self, client):
        """Test deleting non-existent employee"""
        response = client.delete('/employees/999')
        assert response.status_code == 404
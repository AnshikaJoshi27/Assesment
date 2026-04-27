import json
import pytest
from app.models import Employee
from app.db import db


class TestSalaryCalculation:
    """Test salary calculation endpoint"""
    
    def test_salary_calculation_india(self, client):
        """Test salary calculation for India (10% TDS)"""
        employee_data = {
            'full_name': 'Raj Patel',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 100000.0
        }
        
        # Create employee
        create_response = client.post('/employees',
                                    data=json.dumps(employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        # Test salary calculation
        response = client.get(f'/employees/{employee_id}/salary-calculation')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['gross_salary'] == 100000.0
        assert data['tds_deduction'] == 10000.0  # 10% of 100000
        assert data['net_salary'] == 90000.0
    
    def test_salary_calculation_united_states(self, client):
        """Test salary calculation for United States (12% TDS)"""
        employee_data = {
            'full_name': 'John Smith',
            'job_title': 'Software Engineer',
            'country': 'United States',
            'salary': 100000.0
        }
        
        # Create employee
        create_response = client.post('/employees',
                                    data=json.dumps(employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        # Test salary calculation
        response = client.get(f'/employees/{employee_id}/salary-calculation')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['gross_salary'] == 100000.0
        assert data['tds_deduction'] == 12000.0  # 12% of 100000
        assert data['net_salary'] == 88000.0
    
    def test_salary_calculation_other_country(self, client):
        """Test salary calculation for other countries (no deduction)"""
        employee_data = {
            'full_name': 'Hans Mueller',
            'job_title': 'Software Engineer',
            'country': 'Germany',
            'salary': 100000.0
        }
        
        # Create employee
        create_response = client.post('/employees',
                                    data=json.dumps(employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        # Test salary calculation
        response = client.get(f'/employees/{employee_id}/salary-calculation')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['gross_salary'] == 100000.0
        assert data['tds_deduction'] == 0.0  # No deduction for other countries
        assert data['net_salary'] == 100000.0
    
    def test_salary_calculation_case_insensitive_country(self, client):
        """Test that country matching is case insensitive"""
        employee_data = {
            'full_name': 'Raj Patel',
            'job_title': 'Software Engineer',
            'country': 'INDIA',  # Uppercase
            'salary': 100000.0
        }
        
        # Create employee
        create_response = client.post('/employees',
                                    data=json.dumps(employee_data),
                                    content_type='application/json')
        employee_id = json.loads(create_response.data)['id']
        
        # Test salary calculation
        response = client.get(f'/employees/{employee_id}/salary-calculation')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['tds_deduction'] == 10000.0  # Should still apply 10% TDS
    
    def test_salary_calculation_employee_not_found(self, client):
        """Test salary calculation for non-existent employee"""
        response = client.get('/employees/999/salary-calculation')
        assert response.status_code == 404
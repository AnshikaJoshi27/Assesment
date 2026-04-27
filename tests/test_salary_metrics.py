import json
import pytest
from app.models import Employee
from app.db import db


class TestSalaryMetrics:
    """Test salary metrics endpoints"""
    
    def setup_test_employees(self, client):
        """Helper method to set up test employees"""
        employees = [
            {
                'full_name': 'Raj Patel',
                'job_title': 'Software Engineer',
                'country': 'India',
                'salary': 80000.0
            },
            {
                'full_name': 'Priya Singh',
                'job_title': 'Senior Software Engineer',
                'country': 'India',
                'salary': 120000.0
            },
            {
                'full_name': 'John Smith',
                'job_title': 'Software Engineer',
                'country': 'United States',
                'salary': 100000.0
            },
            {
                'full_name': 'Jane Doe',
                'job_title': 'Product Manager',
                'country': 'United States',
                'salary': 150000.0
            },
            {
                'full_name': 'Hans Mueller',
                'job_title': 'Software Engineer',
                'country': 'Germany',
                'salary': 90000.0
            }
        ]
        
        for emp_data in employees:
            client.post('/employees',
                       data=json.dumps(emp_data),
                       content_type='application/json')
    
    def test_country_salary_metrics(self, client):
        """Test salary metrics by country"""
        self.setup_test_employees(client)
        
        # Test India metrics
        response = client.get('/salary-metrics/country/India')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['country'] == 'India'
        assert data['minimum_salary'] == 80000.0
        assert data['maximum_salary'] == 120000.0
        assert data['average_salary'] == 100000.0  # (80000 + 120000) / 2
        assert data['employee_count'] == 2
    
    def test_country_salary_metrics_single_employee(self, client):
        """Test country metrics with single employee"""
        employee_data = {
            'full_name': 'Solo Developer',
            'job_title': 'Full Stack Developer',
            'country': 'Canada',
            'salary': 95000.0
        }
        
        client.post('/employees',
                   data=json.dumps(employee_data),
                   content_type='application/json')
        
        response = client.get('/salary-metrics/country/Canada')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['minimum_salary'] == 95000.0
        assert data['maximum_salary'] == 95000.0
        assert data['average_salary'] == 95000.0
        assert data['employee_count'] == 1
    
    def test_country_salary_metrics_not_found(self, client):
        """Test country metrics for non-existent country"""
        response = client.get('/salary-metrics/country/NonExistentCountry')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'NonExistentCountry' in data['error']
    
    def test_job_title_salary_metrics(self, client):
        """Test salary metrics by job title"""
        self.setup_test_employees(client)
        
        # Test Software Engineer metrics (3 employees: 80000, 100000, 90000)
        response = client.get('/salary-metrics/job-title/Software Engineer')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['job_title'] == 'Software Engineer'
        assert data['average_salary'] == 90000.0  # (80000 + 100000 + 90000) / 3
        assert data['employee_count'] == 3
    
    def test_job_title_salary_metrics_single_employee(self, client):
        """Test job title metrics with single employee"""
        self.setup_test_employees(client)
        
        # Test Product Manager metrics (1 employee: 150000)
        response = client.get('/salary-metrics/job-title/Product Manager')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['job_title'] == 'Product Manager'
        assert data['average_salary'] == 150000.0
        assert data['employee_count'] == 1
    
    def test_job_title_salary_metrics_not_found(self, client):
        """Test job title metrics for non-existent job title"""
        response = client.get('/salary-metrics/job-title/NonExistentTitle')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'NonExistentTitle' in data['error']
    
    def test_job_title_salary_metrics_url_encoding(self, client):
        """Test job title metrics with spaces in title"""
        employee_data = {
            'full_name': 'Senior Dev',
            'job_title': 'Senior Software Engineer',
            'country': 'India',
            'salary': 120000.0
        }
        
        client.post('/employees',
                   data=json.dumps(employee_data),
                   content_type='application/json')
        
        # Test with URL encoded job title
        response = client.get('/salary-metrics/job-title/Senior%20Software%20Engineer')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['job_title'] == 'Senior Software Engineer'
        assert data['average_salary'] == 120000.0
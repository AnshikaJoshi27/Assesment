"""
REST API Routes for Salary Management System

This module defines functions for handling HTTP requests with comprehensive
exception handling for robust error management.

All functions handle specific HTTP endpoints and return JSON responses.
"""

from flask import request, jsonify
from app.db import db
from app.models import Employee, EmployeeSchema
from marshmallow import ValidationError

# Create schema instances for serialization/validation
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# ===== ROUTE REGISTRATION =====

def setup_routes(app):
    """
    Setup all routes using Flask decorators.
    This is cleaner than manual route registration.
    
    Args:
        app (Flask): Flask application instance
    """
    
    # ===== EMPLOYEE CRUD OPERATIONS =====
    
    @app.route('/employees', methods=['POST'])
    def create_employee():
        """Create a new employee - POST /employees"""
        try:
            employee_data = employee_schema.load(request.json)
            employee = Employee(**employee_data)
            db.session.add(employee)
            db.session.commit()
            return jsonify(employee_schema.dump(employee)), 201
        except ValidationError as err:
            return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
        except Exception as err:
            db.session.rollback()
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    @app.route('/employees', methods=['GET'])
    def get_employees():
        """Get all employees - GET /employees"""
        try:
            employees = Employee.query.all()
            return jsonify(employees_schema.dump(employees))
        except Exception as err:
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    @app.route('/employees/<int:employee_id>', methods=['GET'])
    def get_employee(employee_id):
        """Get employee by ID - GET /employees/<id>"""
        try:
            employee = Employee.query.get_or_404(employee_id)
            return jsonify(employee_schema.dump(employee))
        except Exception as err:
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    @app.route('/employees/<int:employee_id>', methods=['PUT'])
    def update_employee(employee_id):
        """Update employee - PUT /employees/<id>"""
        try:
            employee = Employee.query.get_or_404(employee_id)
            employee_data = employee_schema.load(request.json)
            
            for key, value in employee_data.items():
                setattr(employee, key, value)
            
            db.session.commit()
            return jsonify(employee_schema.dump(employee))
        except ValidationError as err:
            return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
        except Exception as err:
            db.session.rollback()
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    @app.route('/employees/<int:employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        """Delete employee - DELETE /employees/<id>"""
        try:
            employee = Employee.query.get_or_404(employee_id)
            db.session.delete(employee)
            db.session.commit()
            return '', 204
        except Exception as err:
            db.session.rollback()
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    # ===== SALARY CALCULATION =====

    @app.route('/employees/<int:employee_id>/salary-calculation', methods=['GET'])
    def calculate_salary(employee_id):
        """Calculate salary - GET /employees/<id>/salary-calculation"""
        try:
            employee = Employee.query.get_or_404(employee_id)
            salary_calculation = employee.calculate_net_salary()
            return jsonify(salary_calculation)
        except Exception as err:
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    # ===== SALARY METRICS =====

    @app.route('/salary-metrics/country/<country>', methods=['GET'])
    def get_country_salary_metrics(country):
        """Get country metrics - GET /salary-metrics/country/<country>"""
        try:
            employees = Employee.query.filter_by(country=country).all()
            
            if not employees:
                return jsonify({'error': f'No employees found for country: {country}'}), 404
            
            salaries = [emp.salary for emp in employees]
            return jsonify({
                'country': country,
                'minimum_salary': min(salaries),
                'maximum_salary': max(salaries),
                'average_salary': sum(salaries) / len(salaries),
                'employee_count': len(employees)
            })
        except Exception as err:
            return jsonify({'error': 'Server error', 'message': str(err)}), 500

    @app.route('/salary-metrics/job-title/<job_title>', methods=['GET'])
    def get_job_title_salary_metrics(job_title):
        """Get job title metrics - GET /salary-metrics/job-title/<job_title>"""
        try:
            employees = Employee.query.filter_by(job_title=job_title).all()
            
            if not employees:
                return jsonify({'error': f'No employees found for job title: {job_title}'}), 404
            
            salaries = [emp.salary for emp in employees]
            return jsonify({
                'job_title': job_title,
                'average_salary': sum(salaries) / len(salaries),
                'employee_count': len(employees)
            })
        except Exception as err:
            return jsonify({'error': 'Server error', 'message': str(err)}), 500
    
    print("All routes setup using decorators")
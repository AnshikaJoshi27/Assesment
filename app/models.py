"""
Data Models and Schemas

This module defines:
1. Employee model - SQLAlchemy database model with business logic
2. EmployeeSchema - Marshmallow schema for validation and serialization

The Employee model contains the core business logic for salary calculations
with country-specific tax deduction rules.
"""

from app.db import db
from marshmallow import Schema, fields, validate


class Employee(db.Model):
    """
    Employee database model.
    
    Represents an employee record with personal information, job details,
    and salary information. Includes business logic for calculating
    net salary based on country-specific tax deduction rules.
    
    Attributes:
        id (int): Primary key, auto-generated
        full_name (str): Employee's full name (max 100 chars)
        job_title (str): Employee's job title (max 100 chars)
        country (str): Employee's country (max 50 chars)
        salary (float): Employee's gross salary (must be positive)
    """
    
    # Database columns with constraints
    id = db.Column(db.Integer, primary_key=True)                    # Auto-incrementing primary key
    full_name = db.Column(db.String(100), nullable=False)           # Required, max 100 characters
    job_title = db.Column(db.String(100), nullable=False)           # Required, max 100 characters
    country = db.Column(db.String(50), nullable=False)              # Required, max 50 characters
    salary = db.Column(db.Float, nullable=False)                    # Required, positive number
    
    def __repr__(self):
        """
        String representation of Employee object.
        
        Makes debugging easier by showing meaningful object representation
        instead of memory address when printing or logging Employee objects.
        
        Returns:
            str: Formatted string showing employee name
        """
        return f'<Employee {self.full_name}>'
    
    def calculate_net_salary(self):
        """
        Calculate net salary based on country-specific tax deduction rules.
        
        Tax Deduction Schedule (TDS - Tax Deducted at Source):
        - India: 10% of gross salary
        - United States: 12% of gross salary  
        - All other countries: 0% (no deductions)
        
        Returns:
            dict: Dictionary containing:
                - gross_salary (float): Original salary amount
                - tds_deduction (float): Tax amount deducted
                - net_salary (float): Salary after tax deduction
                
        Example:
            >>> employee = Employee(salary=100000, country="India")
            >>> result = employee.calculate_net_salary()
            >>> result
            {
                'gross_salary': 100000.0,
                'tds_deduction': 10000.0,
                'net_salary': 90000.0
            }
        """
        gross = self.salary
        
        # Apply country-specific tax deduction rules
        # Using .lower() for case-insensitive comparison
        if self.country.lower() == 'india':
            tds = gross * 0.10  # 10% TDS for India
        elif self.country.lower() == 'united states':
            tds = gross * 0.12  # 12% TDS for United States
        else:
            tds = 0.0           # No deductions for all other countries
        
        return {
            'gross_salary': gross,
            'tds_deduction': tds,
            'net_salary': gross - tds
        }


class EmployeeSchema(Schema):
    """
    Marshmallow schema for Employee model validation and serialization.
    
    This schema handles:
    1. Input validation when creating/updating employees
    2. Data serialization when sending responses to API clients
    3. Type conversion (e.g., string to float for salary)
    
    Validation Rules:
    - All fields except 'id' are required
    - Strings must be non-empty and within length limits
    - Salary must be a positive number
    - ID is auto-generated and only included in output
    """
    
    # Field definitions with validation rules
    id = fields.Int(dump_only=True)                                           # Output only, auto-generated
    full_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))  # Required, 1-100 chars
    job_title = fields.Str(required=True, validate=validate.Length(min=1, max=100))  # Required, 1-100 chars
    country = fields.Str(required=True, validate=validate.Length(min=1, max=50))     # Required, 1-50 chars
    salary = fields.Float(required=True, validate=validate.Range(min=0))             # Required, positive number
"""
Data Models and Schemas

This module defines:
1. Employee model - SQLAlchemy database model with business logic
2. EmployeeCreate/EmployeeResponse - Pydantic schemas for validation and serialization

The Employee model contains the core business logic for salary calculations
with country-specific tax deduction rules.
"""

from app.db import db
from pydantic import BaseModel, Field, validator
from typing import Optional


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


class EmployeeCreate(BaseModel):
    """
    Pydantic schema for creating/updating employees.
    
    This schema handles input validation when creating or updating employees.
    
    Validation Rules:
    - All fields are required
    - Strings must be non-empty and within length limits
    - Salary must be a positive number
    """
    
    full_name: str = Field(..., min_length=1, max_length=100, description="Employee's full name")
    job_title: str = Field(..., min_length=1, max_length=100, description="Employee's job title")
    country: str = Field(..., min_length=1, max_length=50, description="Employee's country")
    salary: float = Field(..., gt=0, description="Employee's gross salary (must be positive)")
    
    @validator('full_name', 'job_title', 'country')
    def validate_strings_not_empty(cls, v):
        """Ensure string fields are not empty or just whitespace"""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or contain only whitespace')
        return v.strip()


class EmployeeResponse(BaseModel):
    """
    Pydantic schema for employee API responses.
    
    This schema handles data serialization when sending responses to API clients.
    Includes all employee fields including the auto-generated ID.
    """
    
    id: int = Field(..., description="Employee ID (auto-generated)")
    full_name: str = Field(..., description="Employee's full name")
    job_title: str = Field(..., description="Employee's job title")
    country: str = Field(..., description="Employee's country")
    salary: float = Field(..., description="Employee's gross salary")
    
    class Config:
        from_attributes = True  # Allows creation from SQLAlchemy models
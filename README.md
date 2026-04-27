# Incubyte Salary Management API

A RESTful API for managing employee data and calculating salary metrics with country-specific tax deductions.

## Features

- **Employee CRUD Operations**: Create, read, update, and delete employee records
- **Salary Calculations**: Calculate net salary with country-specific tax deductions
- **Salary Metrics**: Get salary statistics by country and job title
- **SQLite Database**: Persistent data storage
- **Comprehensive Testing**: Full test coverage following TDD principles

## API Endpoints

### Employee CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/employees` | Create a new employee |
| GET | `/employees` | Get all employees |
| GET | `/employees/{id}` | Get employee by ID |
| PUT | `/employees/{id}` | Update employee by ID |
| DELETE | `/employees/{id}` | Delete employee by ID |

### Salary Calculation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees/{id}/salary-calculation` | Calculate net salary for employee |

### Salary Metrics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/salary-metrics/country/{country}` | Get salary metrics by country |
| GET | `/salary-metrics/job-title/{job_title}` | Get average salary by job title |

## Tax Deduction Rules

- **India**: 10% TDS
- **United States**: 12% TDS
- **Other countries**: No deductions (net = gross)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd salary-management-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python main.py
```

The application will create a SQLite database file (`salary_management.db`) automatically.

### Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:5000`

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_employee_crud.py
```

## API Usage Examples

### Create Employee

```bash
curl -X POST http://localhost:5000/employees \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "job_title": "Software Engineer", 
    "country": "India",
    "salary": 100000.0
  }'
```

### Get All Employees

```bash
curl -X GET http://localhost:5000/employees
```

### Calculate Salary

```bash
curl -X GET http://localhost:5000/employees/1/salary-calculation
```

### Get Country Metrics

```bash
curl -X GET http://localhost:5000/salary-metrics/country/India
```

### Get Job Title Metrics

```bash
curl -X GET http://localhost:5000/salary-metrics/job-title/Software%20Engineer
```

## Response Examples

### Employee Object
```json
{
  "id": 1,
  "full_name": "John Doe",
  "job_title": "Software Engineer",
  "country": "India", 
  "salary": 100000.0
}
```

### Salary Calculation
```json
{
  "gross_salary": 100000.0,
  "tds_deduction": 10000.0,
  "net_salary": 90000.0
}
```

### Country Metrics
```json
{
  "country": "India",
  "minimum_salary": 80000.0,
  "maximum_salary": 120000.0,
  "average_salary": 100000.0,
  "employee_count": 2
}
```

### Job Title Metrics
```json
{
  "job_title": "Software Engineer",
  "average_salary": 95000.0,
  "employee_count": 3
}
```

## Implementation Details

### AI Usage

This project was developed following best practices with AI assistance for:

1. **Code Scaffolding**: Used AI to generate initial Flask project structure and boilerplate code
2. **Test Generation**: AI helped create comprehensive test suites covering all endpoints and edge cases
3. **API Design**: AI assisted in designing RESTful endpoints following industry standards
4. **Documentation**: AI helped generate comprehensive API documentation and examples

### TDD Approach

The project strictly follows Test-Driven Development:

1. **Red**: Write failing tests first for each feature
2. **Green**: Implement minimal code to pass tests
3. **Refactor**: Improve code quality while keeping tests green

Commit history reflects the TDD cycle with incremental development.

### Architecture

- **Flask**: Web framework for API development
- **SQLAlchemy**: ORM for database operations
- **Marshmallow**: Data serialization and validation
- **pytest**: Testing framework
- **SQLite**: Lightweight database for development

### Project Structure

```
salary-management-api/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models.py            # Database models and schemas
│   └── routes.py            # API endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_employee_crud.py
│   ├── test_salary_calculation.py
│   └── test_salary_metrics.py
├── main.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Production Considerations

- Configure proper environment variables for production
- Use PostgreSQL or MySQL for production database
- Implement authentication and authorization
- Add rate limiting and request validation
- Set up proper logging and monitoring
- Use WSGI server like Gunicorn for production deployment
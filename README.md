# Gas Utility Service API

A Django REST API for managing gas utility service requests and user accounts. This system provides a comprehensive solution for gas utility companies to handle customer service requests, manage user accounts, and streamline administrative tasks.

## Features

### For Customers
- **User Registration & Authentication**
  - Secure account creation with unique customer IDs
  - Login system with session-based authentication
  - Profile management with personal information

- **Service Request Management**
  - Submit new service requests (New Connection, Maintenance, etc.)
  - Track request status and history
  - View request details and updates

### For Administrators
- **User Management**
  - View all registered users
  - Create new user accounts
  - Update user information
  - Delete user accounts

- **Service Request Administration**
  - View all service requests
  - Update request status
  - Add resolution details
  - Delete service requests

### Security Features
- CSRF protection for all API endpoints
- Session-based authentication
- Role-based access control
- Secure password handling
- Input validation and sanitization

### Technical Features
- RESTful API architecture
- MySQL database integration
- Environment-based configuration
- Comprehensive error handling
- JSON response format

## Project Structure
```
gas_utility/
├── accounts/                    # User management app
│   ├── migrations/             # Database migrations
│   ├── __init__.py
│   ├── admin.py               # Admin configuration
│   ├── apps.py
│   ├── forms.py               # User forms
│   ├── models.py              # Custom user model
│   ├── urls.py                # URL routing
│   └── views.py               # View logic
├── utility_services/          # Service request management app
│   ├── migrations/            # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py
│   ├── models.py             # Service request model
│   ├── urls.py               # URL routing
│   └── views.py              # View logic
├── gas_utility/              # Project settings
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── manage.py
└── .env                     # Environment variables
```

## Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd gas_utility-service
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django djangorestframework mysqlclient python-dotenv
```

4. Create MySQL database:
```sql
CREATE DATABASE gas_utility_db;
```

5. Configure environment variables in `.env`:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=gas_utility_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

6. Apply migrations:
```bash
cd gas_utility
python manage.py migrate
```

7. Create superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

### Authentication
All endpoints except registration and login require authentication. Include the CSRF token in the header for authenticated requests.

### User Management

#### 1. Register New User
```
POST /accounts/api/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password1": "password123",
    "password2": "password123",
    "name": "Test User",
    "phone_number": "1234567890",
    "address": "123 Test St"
}
```

#### 2. User Login
```
POST /accounts/api/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123"
}
```

#### 3. Get Account Information
```
GET /accounts/api/account/
Headers:
  X-CSRFToken: <token from cookie>
```

### Service Request Management

#### 1. Submit Service Request
```
POST /api/submit/
Headers:
  Content-Type: application/json
  X-CSRFToken: <token from cookie>

{
    "type_of_request": "New Connection",
    "details": "Need new gas connection"
}
```

#### 2. Track Requests
```
GET /api/track/
Headers:
  X-CSRFToken: <token from cookie>
```

### Admin Endpoints

#### 1. List All Users
```
GET /accounts/api/admin/users/
Headers:
  X-CSRFToken: <token from cookie>
```

#### 2. Create User (Admin)
```
POST /accounts/api/admin/users/create/
Headers:
  Content-Type: application/json
  X-CSRFToken: <token from cookie>

{
    "username": "newuser",
    "email": "new@example.com",
    "password1": "password123",
    "password2": "password123",
    "name": "New User",
    "phone_number": "1234567890",
    "address": "123 New St"
}
```

#### 3. Get User Details (Admin)
```
GET /accounts/api/admin/users/<user_id>/
Headers:
  X-CSRFToken: <token from cookie>
```

#### 4. Update User (Admin)
```
PUT /accounts/api/admin/users/<user_id>/
Headers:
  Content-Type: application/json
  X-CSRFToken: <token from cookie>

{
    "name": "Updated Name",
    "email": "updated@example.com"
}
```

#### 5. Delete User (Admin)
```
DELETE /accounts/api/admin/users/<user_id>/
Headers:
  X-CSRFToken: <token from cookie>
```

#### 6. List All Service Requests (Admin)
```
GET /api/admin/requests/
Headers:
  X-CSRFToken: <token from cookie>
```

#### 7. Get Request Details (Admin)
```
GET /api/admin/requests/<request_id>/
Headers:
  X-CSRFToken: <token from cookie>
```

#### 8. Update Request (Admin)
```
PUT /api/admin/requests/<request_id>/
Headers:
  Content-Type: application/json
  X-CSRFToken: <token from cookie>

{
    "status": "In Progress",
    "details": "Updated details"
}
```

#### 9. Delete Request (Admin)
```
DELETE /api/admin/requests/<request_id>/
Headers:
  X-CSRFToken: <token from cookie>
```

## Response Formats

### Success Response
```json
{
    "message": "Operation successful",
    "data": {
        // Response data
    }
}
```

### Error Response
```json
{
    "error": "Error message",
    "details": {
        // Error details if available
    }
}
```

## Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 405: Method Not Allowed
- 500: Internal Server Error

## Testing
To test the API endpoints:
1. Start the development server
2. Use Postman or any API testing tool
3. Follow the authentication flow:
   - Register a new user
   - Login to get CSRF token
   - Use the token in subsequent requests

## Security
- CSRF protection enabled
- Session-based authentication
- Admin-only endpoints protected
- Password hashing
- Input validation
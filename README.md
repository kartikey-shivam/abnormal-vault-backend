# Abnormal Vault

A secure vault management system built with Django.

## Setup Instructions

1. Clone the repository
```bash
git clone [repository-url]
cd abnormal_vault
```

2. Create and activate virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
- Create a `.env` file in the root directory
- Add required environment variables (see `.env.example`)

5. Run database migrations
```bash
python manage.py migrate
```

6. Create superuser (admin)
```bash
python manage.py createsuperuser
```

7. Run development server
```bash
python manage.py runserver
```

## Available Routes

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/reset-password/` - Password reset

### Vault Endpoints
- `GET /api/vaults/` - List all vaults
- `POST /api/vaults/` - Create new vault
- `GET /api/vaults/<id>/` - Get specific vault
- `PUT /api/vaults/<id>/` - Update vault
- `DELETE /api/vaults/<id>/` - Delete vault

## Project Structure
```
abnormal_vault/
├── abnormal_vault/        # Project configuration
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── apps/                  # Django applications
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Technology Stack
- Python 3.8+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis (for caching)

## Security Features
- Encryption at rest
- Role-based access control
- Two-factor authentication
- Audit logging
- Session management

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details
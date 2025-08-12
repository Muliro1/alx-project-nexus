# Polling System API

A robust Django REST API for creating polls, voting, and viewing results with comprehensive security features, rate limiting, and GraphQL support.

## 🚀 Features

- **REST API** with comprehensive CRUD operations
- **GraphQL API** for flexible data querying
- **Interactive Home Page** with complete route documentation
- **Token-based Authentication** with secure endpoints
- **Rate Limiting** to prevent API abuse
- **Input Validation & Sanitization** for security
- **Swagger/OpenAPI Documentation** for easy testing
- **CORS Support** for cross-origin requests
- **Security Headers** and HTTPS support
- **PostgreSQL Database** for production-ready data storage

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Security Features](#security-features)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### 1. Clone and Setup
```bash
git clone https://github.com/Muliro1/alx-project-nexus.git
cd alx-project-nexus/polling_system
```

### 2. Environment Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb polling_system_db

# Copy environment file
cp env_example.txt .env

# Edit .env with your database credentials
# Update DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

### 7. Access API Documentation
- **Home Page**: http://localhost:8000/ (Complete route overview)
- **Swagger UI**: http://localhost:8000/api-docs/
- **GraphQL Playground**: http://localhost:8000/graphql/

## 🔧 Detailed Setup

### Environment Variables

Create a `.env` file in the `polling_system` directory:

```bash
# Database Configuration
DB_NAME=polling_system_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# Security Settings
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# CORS Settings
CORS_ORIGIN_ALLOW_ALL=True
```

### Database Configuration

#### PostgreSQL Setup
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE polling_system_db;
CREATE USER polling_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE polling_system_db TO polling_user;
\q
```

#### SQLite (Development Only)
If you prefer SQLite for development, modify `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 📚 API Documentation

### Home Route

#### 1. Home Page
```bash
# GET /
curl http://localhost:8000/
```

**Description**: The home route provides a comprehensive overview of all available API endpoints and features. It renders an interactive HTML template that displays:

- **API Information**: Base URL, authentication details, and links to documentation
- **Authentication Routes**: Token-based authentication endpoints
- **Poll Management Routes**: CRUD operations for polls
- **Voting & User Management**: User registration and voting functionality
- **Admin & Development**: Administrative interfaces and development tools

**Features**:
- Modern, responsive design with hover effects
- Color-coded HTTP methods (GET, POST, PUT, DELETE)
- Direct links to Swagger documentation and GraphQL playground
- Mobile-friendly layout
- Interactive route cards with detailed descriptions

**Access**: No authentication required - publicly accessible

### Authentication

#### 1. Get Authentication Token
```bash
# POST /api-token-auth/
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "token": "your-auth-token-here",
  "user_id": 1
}
```

#### 2. Using the Token
```bash
# Include in headers for authenticated requests
curl -H "Authorization: Token your-auth-token-here" \
  http://localhost:8000/polls/
```

### Poll Management

#### Create a Poll
```bash
# POST /polls/
curl -X POST http://localhost:8000/polls/ \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is your favorite programming language?",
    "expires_at": "2024-12-31T23:59:59Z",
    "options": [
      {"text": "Python"},
      {"text": "JavaScript"},
      {"text": "Java"},
      {"text": "C++"}
    ]
  }'
```

#### List All Polls
```bash
# GET /polls/
curl -H "Authorization: Token your-token" \
  http://localhost:8000/polls/
```

#### View Poll Results
```bash
# GET /polls/{poll_id}/results/
curl http://localhost:8000/polls/1/results/
```

### Voting

#### Vote on an Option
```bash
# POST /polls/vote/
curl -X POST http://localhost:8000/polls/vote/ \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "poll_id": 1,
    "option_id": 2,
    "voter_id": "anonymous_123"
  }'
```

### User Registration

#### Register New User
```bash
# POST /polls/register/
curl -X POST http://localhost:8000/polls/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "SecurePass123",
    "email": "user@example.com"
  }'
```

## 🔐 Security Features

### Authentication & Authorization
- **Token-based authentication** for API access
- **Password strength requirements** (8+ chars, uppercase, lowercase, digit)
- **Username validation** (alphanumeric + underscore only)
- **Email validation** for registration

### Input Validation & Sanitization
- **Input length limits** to prevent buffer overflow
- **Character sanitization** (removes `< > " '`)
- **Poll expiration validation** (no voting on expired polls)
- **Option uniqueness validation** (no duplicate options)
- **Vote validation** (prevents duplicate votes)

### Rate Limiting
- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **Burst protection**: 60 requests/minute

### Security Headers
- **X-Content-Type-Options**: nosniff
- **X-Frame-Options**: DENY
- **X-XSS-Protection**: 1; mode=block
- **HSTS headers** (production)
- **Content Security Policy**

### CORS Configuration
- **Configurable origins** for cross-origin requests
- **Restricted HTTP methods** and headers
- **Credentials support** for authenticated requests

## 🚀 Deployment

### Render Deployment

1. **Connect your repository** to Render
2. **Create a new Web Service**
3. **Configure environment variables** in Render dashboard:

```bash
# Required Environment Variables
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

4. **Build Command:**
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

5. **Start Command:**
```bash
gunicorn polling_system.wsgi:application
```

### Other Platforms

#### Heroku
```bash
# Add to requirements.txt
gunicorn==20.1.0
whitenoise==6.2.0

# Create Procfile
echo "web: gunicorn polling_system.wsgi:application" > Procfile

# Deploy
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### DigitalOcean App Platform
- Upload your code
- Configure environment variables
- Set build and run commands

## 🔍 GraphQL API

The system also provides a GraphQL API for flexible data querying:

### Access GraphQL Playground
- **URL**: http://localhost:8000/graphql/
- **Features**: Interactive query builder, schema exploration

### Example Queries

#### Query All Polls
```graphql
query {
  polls {
    id
    question
    expiresAt
    options {
      id
      text
      votes
    }
  }
}
```

#### Query Specific Poll
```graphql
query {
  poll(id: 1) {
    question
    options {
      text
      votes
    }
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Error: Set the DB_NAME environment variable
# Solution: Create .env file with database credentials
cp env_example.txt .env
# Edit .env with your database settings
```

#### 2. Migration Errors
```bash
# Reset migrations (if needed)
python manage.py migrate --fake polls zero
python manage.py migrate --fake-initial
```

#### 3. Authentication Issues
```bash
# Check if user exists
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
```

#### 4. CORS Issues
```bash
# Update CORS settings in .env
CORS_ORIGIN_ALLOW_ALL=True
# Or specify allowed origins:
CORS_ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:3000
```

### Development Commands

```bash
# Run tests
python manage.py test

# Check for security issues
python manage.py check --deploy

# Create database backup
python manage.py dumpdata > backup.json

# Load database backup
python manage.py loaddata backup.json

# Collect static files
python manage.py collectstatic

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## 📊 API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Home page | No |
| POST | `/api-token-auth/` | Get authentication token | No |
| POST | `/polls/register/` | Register new user | No |
| GET | `/polls/` | List all polls | Yes |
| POST | `/polls/` | Create new poll | Yes |
| GET | `/polls/{id}/results/` | View poll results | No |
| POST | `/polls/vote/` | Vote on an option | Yes |
| GET | `/graphql/` | GraphQL playground | No |
| GET | `/api-docs/` | Swagger documentation | No |

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**: `git commit -m 'Add feature'`
6. **Push to the branch**: `git push origin feature-name`
7. **Submit a pull request**

### Development Guidelines

- **Follow PEP 8** for Python code style
- **Write tests** for new features
- **Update documentation** for API changes
- **Use meaningful commit messages**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Muliro1/alx-project-nexus/issues)
- **Documentation**: [API Docs](http://localhost:8000/api-docs/)
- **GraphQL**: [GraphQL Playground](http://localhost:8000/graphql/)

---

**Built with ❤️ using Django REST Framework and GraphQL**
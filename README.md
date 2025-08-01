# MyDuka Backend


A modern, role-based management tool for small retail businesses. This is a robust REST API built with Django and Django REST Framework, designed to be secure, scalable, and easy to maintain.


## 🚀 Features
- **RESTful API** - Clean and intuitive API design
- **Role-based Authentication** - Secure JWT token-based authentication
- **M-Pesa Integration** - Seamless mobile money payments
- **Email Integration** - Automated notifications via SendGrid
- **Auto-generated Documentation** - Interactive API docs with Swagger UI
- **Production Ready** - Configured for deployment on Render

  

## 🛠️ Built With
- Django - Python web framework
- Django REST Framework - Powerful toolkit for building APIs
- Django REST Framework Simple JWT -Token-based authentication
- PostgreSQL - Production database
- Gunicorn - Production WSGI server
- drf-spectacular - Automatic API documentation




## 📋 Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Installation](#-installation)
3. [Database Setup](#-database-setup)
4. [Environment Variables](#-environment-variables)
5. [Running Locally](#-running-locally)
6. [Running Tests](#-running-tests)
7. [API Documentation](#-api-documentation)
8. [Deployment](#-deployment)
9. [M-Pesa Testing](#-mpesa-integration-testing)
10. [Contributing](#-contributing)




## 📋 Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8+
- pip (Python package installer)
- venv (Virtual Environment)

## 🔧 Installation

### Clone the repository
run git clone in terminal

### Navigate to the project directory
- navigate to the myduka direcory:
cd my-duka-backend/myduka

- Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

- Install dependencies:
pip install -r requirements.txt


## 🗄️ Database Setup
Important: Due to model dependencies, follow these steps in order:

1. Clean up existing database:
rm db.sqlite3
rm -rf users/migrations stores/migrations reports/migrations payments/migrations.


2. Run migrations in the correct order:
python manage.py makemigrations stores
python manage.py makemigrations users reports payments
python manage.py migrate

3. Create a superuser:
python manage.py createsuperuser

## 🔐 Environment Variables
Create a .env file in the same directory as settings.py and add the following:


 --- Core Django Settings ---
SECRET_KEY="your-unique-django-secret-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

 --- Database (optional for local development) ---
DATABASE_URL=sqlite:///db.sqlite3

--- CORS Settings ---
CORS_ALLOWED_ORIGINS=http://localhost:5173
CORS_TRUSTED_ORIGINS=http://localhost:5173

 --- Email Configuration (SendGrid) ---
SENDGRID_API_KEY="your-sendgrid-api-key"
DEFAULT_FROM_EMAIL="your-verified-sender@example.com"

### --- M-Pesa Sandbox Credentials ---
MPESA_CONSUMER_KEY="your-daraja-consumer-key"
MPESA_CONSUMER_SECRET="your-daraja-consumer-secret"
MPESA_SHORTCODE=174379
MPESA_PASSKEY="your-daraja-passkey"

### --- Frontend URL ---
FRONTEND_URL=http://localhost:5173

## 🚀 Running Locally
- Start the development server:
python manage.py runserver

- The API will be available at http://127.0.0.1:8000/

## 🧪 Running Tests
- Execute the automated test suite:
python manage.py test


## 📚 API Documentation
This project uses drf-spectacular for automatic API documentation generation.


While your local server is running, access the documentation at:

Swagger UI: http://127.0.0.1:8000/api/v1/docs/

Redoc: http://127.0.0.1:8000/api/v1/redoc/

## 🌐 Deployment to Render
1. Create PostgreSQL Database
Create a new PostgreSQL database on Render

Copy the "Internal Database URL"

2. Create Web Service
Configure your Render Web Service with:

Runtime: Python 3

Root Directory: myduka (folder containing manage.py)

- Build Command:
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py createsuperuser_if_none_exists

- Start Command:
gunicorn myduka.wsgi -c gunicorn.conf.py


3. Environment Variables
Set the following environment variables in your Render Web Service:


DATABASE_URL=your-render-postgresql-internal-url
ALLOWED_HOSTS=myduka-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://www.myduka.online
FRONTEND_URL=https://www.myduka.online.
# ... plus all other variables from your .env file

# For automatic superuser creation on first deploy
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your-secure-password
💳 M-Pesa Integration Testing
To test M-Pesa callbacks locally, you need to expose your local server:

- Download and run ngrok:
./ngrok http 8000

- Get the public URL:
ngrok will provide a public https://... URL ..

- Update callback URL:
In myduka/payments/views.py, temporarily replace the callback_url with your ngrok URL

### 🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request


## Access my documentation
https://my-duka-backend.onrender.com/api/v1/docs/

Made by the following:
1. Adrian Maina
2. Emmanuel Ontweka
3. Benard Kimari
4. Ian Githae
5. Ignatius Kamau


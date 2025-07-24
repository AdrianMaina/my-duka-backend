# FILE: README.md 

# MyDuka - Backend (Django REST Framework)

This is the DRF backend for MyDuka, providing a RESTful API for the frontend application.

## ✨ Features

* Secure, versioned REST API.
* JWT Authentication with SimpleJWT.
* Role-based access control (Merchants, Admins, Clerks).
* API endpoints for managing stores and inventory.
* Tokenized invitation system for Admins and Clerks.
* Placeholder for M-Pesa integration.

## 🚀 Getting Started

### 1. Setup

1.  **Clone the repository:**
    `git clone <repository-url> && cd myduka-backend`
2.  **Create a virtual environment and activate it:**
    `python3 -m venv venv`
    `source venv/bin/activate`
3.  **Install dependencies:**
    `pip install -r requirements.txt`
4.  **Create a `.env` file** in the `myduka/` directory (alongside `settings.py`). Copy the contents of the `.env` template and fill in your details.
5.  **Clean Up (IMPORTANT for fixing errors):** If you have run commands before, delete the `db.sqlite3` file and the `migrations` folders inside the `users` and `stores` apps to start fresh.
6.  **Create migration files for your apps (in order):**
    `python manage.py makemigrations users`
    `python manage.py makemigrations stores`
7.  **Run database migrations to create the tables:**
    `python manage.py migrate`
8.  **Create a superuser** to access the Django Admin:
    `python manage.py createsuperuser`
9.  **Run the development server:**
    `python manage.py runserver`

The API will be available at `http://127.0.0.1:8000/api/v1/`.

## 🔧 M-Pesa Development Setup

The M-Pesa API needs to send a confirmation (callback) to your server. Since your server is running locally, you need to expose it to the internet.

1.  **Download ngrok:** [https://ngrok.com/download](https://ngrok.com/download)
2.  **Run ngrok** to expose your Django port (usually 8000):
    `./ngrok http 8000`
3.  **ngrok will give you a public URL** (e.g., `https://random-string.ngrok.io`). This is your public base URL.
4.  **On the Daraja Portal:** When registering your callback URLs, use the ngrok URL. For example:
    * Confirmation URL: `https://random-string.ngrok.io/api/v1/mpesa/confirm/`
    * Validation URL: `https://random-string.ngrok.io/api/v1/mpesa/validate/`

## ✉️ Email Invite Setup

1.  **Sign up for SendGrid** or a similar email service.
2.  Get your API key.
3.  Add `SENDGRID_API_KEY` and `DEFAULT_FROM_EMAIL` to your `.env` file.
4.  In `myduka/settings.py`, change the `EMAIL_BACKEND` to use the SendGrid backend (see their documentation for specifics).
5.  Create a `users/utils.py` file and implement the `send_invite_email` function to send the actual email.

By Ian Githae.
By Benard Kimari.
By Adrian Maina.

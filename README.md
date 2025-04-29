# Django SaaS Application

This project is a Django-based SaaS (Software as a Service) application designed to provide a robust foundation for building subscription-based web applications. It includes features such as user authentication, subscription management, dashboards, and more.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Templates Overview](#templates-overview)
- [Key Models](#key-models)
- [Key Views](#key-views)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Features

- User authentication and registration (via Django Allauth).
- Subscription management with Stripe integration.
- Dashboard for users to manage their accounts and subscriptions.
- Page visit tracking and analytics.
- Role-based access control for protected views.
- Responsive design with reusable templates.
- Integration with third-party tools like GitHub OAuth and Stripe.

---

## Project Structure

```
.
├── .env                     # Environment variables
├── .gitignore               # Git ignore file
├── Dockerfile               # Docker configuration
├── railway.toml             # Railway deployment configuration
├── requirements.txt         # Python dependencies
├── src/                     # Main application directory
│   ├── manage.py            # Django management script
│   ├── db.sqlite3           # SQLite database (for development)
│   ├── auth/                # User authentication app
│   ├── checkouts/           # Checkout and payment processing
│   ├── commando/            # Custom commands and utilities
│   ├── customers/           # Customer management
│   ├── dashboard/           # User dashboard
│   ├── helpers/             # Utility functions (e.g., billing)
│   ├── landing/             # Landing page templates
│   ├── profiles/            # User profiles
│   ├── saas/                # Core project settings and URLs
│   ├── staticfiles/         # Static assets
│   ├── subscriptions/       # Subscription management
│   ├── templates/           # HTML templates
│   ├── visits/              # Page visit tracking
│   └── migrations/          # Database migrations
└── .github/                 # GitHub workflows for CI/CD
    └── workflows/           # YAML files for GitHub Actions
```

---

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd django-saas-re
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and configure the required variables (e.g., database credentials, Stripe API keys).

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

---

## Environment Variables

The `.env` file should include the following variables:

- `SECRET_KEY`: Django secret key.
- `DEBUG`: Set to `True` for development.
- `DATABASE_URL`: Database connection string.
- `STRIPE_API_KEY`: Stripe API key for payment processing.
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts.

---

## Usage

### Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000`.

### Running Tests

To run the test suite:
```bash
python manage.py test
```

---

## Templates Overview

The project uses Django templates for rendering HTML. Key templates include:

- **Landing Pages**:
  - `landing/main.html`: Main landing page.
  - `landing/hero.html`: Hero section.
  - `landing/features.html`: Features section.
  - `landing/proof.html`: Social proof section.

- **Authentication**:
  - `auth/register.html`: User registration form.

- **Dashboard**:
  - `dashboard/base.html`: Base template for the dashboard.
  - `dashboard/nav.html`: Navigation bar for the dashboard.
  - `dashboard/main.html`: Main dashboard content.

- **Protected Views**:
  - `protected/entry.html`: Password-protected entry page.
  - `protected/user-required.html`: User-only access page.
  - `protected/staff-required.html`: Staff-only access page.

- **Subscriptions**:
  - `subscriptions/user_detail_view.html`: User subscription details.

---

## Key Models

### `PageVisits` (in `visits` app)
Tracks page visits and stores the path and timestamp.

### `Subscription` (in `subscriptions` app)
Manages subscription plans and user subscriptions.

---

## Key Views

### `home_view` (in `src/saas/views.py`)
Tracks page visits and calculates the percentage of total visits for the current page.

### `checkout_finalize_view` (in `src/checkouts/views.py`)
Handles the finalization of user subscriptions and updates Stripe data.

---

## Testing

The project includes unit tests for various components. Tests are located in the `tests.py` files within each app directory.

To run all tests:
```bash
python manage.py test
```

---

## Deployment

### Railway
The `railway.toml` file is configured for deployment on Railway.

### GitHub Actions
CI/CD workflows are defined in `.github/workflows/` for automated testing and deployment.

---

## License

This project is licensed under the MIT License.

---

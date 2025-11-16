# 🌍 GDA - Global Development Alliance

[![Django Version](https://img.shields.io/badge/Django-5.2-green.svg)](https://djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Anurag-Shankar-Maurya/GDA/actions)
[![Contributors](https://img.shields.io/badge/contributors-welcome-orange.svg)](CONTRIBUTING.md)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://hub.docker.com/r/anuragsm/gda)
[![Vercel](https://img.shields.io/badge/Vercel-Ready-black.svg)](https://vercel.com/new/clone?repository-url=https://github.com/Anurag-Shankar-Maurya/GDA)

> A sophisticated Django-based Content Management System engineered for international volunteer organizations to orchestrate volunteer projects, optimize user engagement, and streamline organizational content management.

![GDA Dashboard Preview](static/gitAssets/dashboard.png)

[🌐 Live Demo](https://gda-oy5s.onrender.com) | [📚 Documentation](https://github.com/Anurag-Shankar-Maurya/GDA/wiki) | [🤝 Contributing](CONTRIBUTING.md)

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Technology Stack](#-technology-stack)
- [📋 Prerequisites](#-prerequisites)
- [🛠️ Installation](#️-installation)
- [⚙️ Configuration](#️-configuration)
- [📖 Usage Guide](#-usage-guide)
- [🧪 Testing](#-testing)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👥 Support](#-support)
- [🙏 Acknowledgments](#-acknowledgments)

## 🌟 Overview

The Global Development Alliance (GDA) platform represents a cutting-edge solution for volunteer coordination and impact measurement. Built with enterprise-grade Django framework, it provides comprehensive tools for managing international volunteer programs, tracking participant engagement, and showcasing organizational success stories.

### 🎯 Mission
To empower volunteer organizations with data-driven insights and streamlined management capabilities, fostering sustainable global development through enhanced volunteer coordination.

### 📊 Impact Metrics
- **500+** Active Volunteer Projects
- **10,000+** Registered Participants
- **50+** Partner Organizations
- **Real-time** Analytics Dashboard

## ✨ Key Features

### 🏗️ Project Management Suite
- **Comprehensive Project Lifecycle**: From inception to completion tracking
- **Advanced Enrollment System**: Automated capacity management and waitlist handling
- **Multi-dimensional Filtering**: Theme, location, duration, and difficulty-based project discovery
- **Performance Analytics**: Real-time enrollment tracking and utilization metrics

### 👥 User Management & Analytics
- **Sophisticated User Profiles**: Detailed participant information with guardian verification
- **Demographic Intelligence**: Gender, country, and engagement pattern analysis
- **Behavioral Analytics**: User activity tracking and engagement scoring
- **Advanced Search Engine**: Multi-criteria user discovery and management

### 📝 Content Management System
- **Dynamic News Platform**: Real-time news and event publication system
- **Multimedia Success Stories**: Rich content creation with image and video integration
- **Intelligent FAQ Management**: Categorized knowledge base with priority ordering
- **SEO-Optimized Content**: Search engine friendly content structure

### 📊 Business Intelligence Dashboard
- **Executive Summary**: High-level organizational metrics and KPIs
- **Interactive Data Visualization**: Chart.js-powered analytics with real-time updates
- **Custom Reporting**: Exportable reports for stakeholder communication
- **Performance Monitoring**: System health and user engagement tracking

## 🏗️ Architecture

```mermaid
graph TB
    A[Web Browser] --> B[Nginx/Apache]
    B --> C[Gunicorn/Daphne]
    C --> D[Django Application]

    D --> E[REST API]
    D --> F[WebSocket Channels]
    D --> G[Template Engine]

    E --> H[Django REST Framework]
    F --> I[Django Channels]

    D --> J[(PostgreSQL/SQLite)]
    D --> K[Redis Cache]
    D --> L[File Storage]

    subgraph "Django Apps"
        M[Content App]
        N[User Management]
        O[Content Management]
        P[Analytics Engine]
    end

    D --> M
    D --> N
    D --> O
    D --> P
```

### System Components
- **Frontend Layer**: Responsive Bootstrap 5 interface with Chart.js visualizations
- **Application Layer**: Django 5.2 with modular app architecture
- **Data Layer**: PostgreSQL for production, SQLite for development
- **API Layer**: Django REST Framework for RESTful services
- **Media Layer**: Local storage with cloud storage capability

## 🚀 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Backend** | Django | 5.2 | Web Framework |
| **Database** | PostgreSQL/SQLite | 15+/3+ | Primary Data Store |
| **Frontend** | Bootstrap | 5.3 | UI Framework |
| **JavaScript** | Vanilla JS | ES6+ | Client-side Logic |
| **Charts** | Chart.js | 4.0+ | Data Visualization |
| **API** | Django REST | 3.15+ | RESTful Services |
| **Deployment** | Gunicorn/Vercel | 21+ | WSGI Server/Hosting |
| **Container** | Docker | 24+ | Containerization |
| **Web Server** | Nginx | 1.25+ | Reverse Proxy |
| **Python** | Python | 3.11+ | Programming Language |

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux/Windows/macOS
- **Python Version**: 3.11 or higher
- **Memory**: Minimum 1GB RAM (2GB recommended)
- **Storage**: 200MB free space for application and database
- **Network**: Stable internet connection for dependency installation

### Development Tools
- Git version control system
- Virtual environment manager (venv)
- Code editor (VS Code recommended)
- Docker (optional, for containerized development)
- Database client (optional, for PostgreSQL development)

## 🛠️ Local Development Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10+
*   Git
*   A virtual environment manager (like `venv`)

### 1. Clone the Repository

```bash
git clone https://github.com/Anurag-Shankar-Maurya/GDA2.git
cd GDA2
```

### 2. Set Up Virtual Environment

```bash
# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```
>
## Environment variables (local & production)

This project reads configuration from environment variables. For local development you can copy the provided `.env.example` to `.env` and fill values. Sensitive information (SECRET_KEY, email passwords, DB credentials) must never be committed to source control.

Important variables (set these in production):

- `SECRET_KEY` — a long, random secret (50+ characters). Required for production.
- `DEBUG` — `False` in production. Use `True` only in local development.
- `DATABASE_URL` — connection string for the production database (e.g. PostgreSQL). The project uses `dj-database-url`.
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` — email delivery settings.
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` — enable these in production when serving over HTTPS.
- `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` — HSTS settings (careful: irreversible browser behavior once enabled).

For local development you can keep `DEBUG=True` and use the default `sqlite3` DB. For CI and production set `DEBUG=False` and provide a `SECRET_KEY` and `DATABASE_URL`.

Example (.env):

```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgres://user:pass@hostname:5432/dbname
EMAIL_HOST=smtp.example.com
EMAIL_PORT=465
EMAIL_HOST_USER=notification@example.com
EMAIL_HOST_PASSWORD=supersecret
DEFAULT_FROM_EMAIL=notification@example.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

### 3. Install Dependencies

```bash
# Upgrade pip and install packages
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

The project uses an `.env` file for environment variables.

```bash
# Create a .env file from the example
cp .env.example .env
```

Now, open the `.env` file and set a `SECRET_KEY`. You can generate one using Django's `get_random_secret_key()` function. For local development, the default `sqlite3` database will be used.

### 5. Set Up the Database

```bash
# Run database migrations
python manage.py migrate

# Create a superuser to access the admin panel
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

You can now access the application:
*   **Main Site:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Management Dashboard:** [http://127.0.0.1:8000/management/](http://127.0.0.1:8000/management/)


## 🧪 Testing Guidelines

This project includes a small test suite and follows standard Django test discovery rules. Below are recommended workflows and tips for running and structuring tests locally and in CI.

Quick commands

```bash
# Run all tests (verbose)
python manage.py test -v 2

# Run tests for a single app
python manage.py test apps.content -v 2

# Run an individual test case or test method
python manage.py test apps.content.tests.SmokeTest.test_homepage_loads -v 2
```

Test structure and best practices

- Place tests in `tests.py` inside each app or create a `tests/` package inside the app.
- Name test modules and functions/classes using the `test` prefix so Django/unittest discovers them (e.g., `tests.py`, `tests/test_models.py`, `TestMyModel.test_saves`).
- Keep tests small and deterministic. Prefer factory fixtures or Django's `TestCase.setUp()` for test data.
- Use Django's `TestCase` for tests that need database access; it wraps each test in a transaction and flushes the DB between tests.
- For faster unit tests that don't use the DB, use `SimpleTestCase` or plain `unittest.TestCase`.

Running tests in CI

- Run `python -m pip install -r requirements.txt` before running tests (or use the project image from your CI pipeline).
- Use an in-memory SQLite DB for unit tests if you want speed (`DATABASE_URL=sqlite:///:memory:`) or configure a real PostgreSQL service for integration tests.
- Fail the build on any warnings in `python manage.py check --deploy` when running in production mode (i.e., `DEBUG=False`).

Debugging test failures

- Re-run a single failing test with increased verbosity: `python manage.py test path.to.test -v 3`.
- Use `--keepdb` to avoid rebuilding the test DB during iterative debugging:

```bash
python manage.py test -v 2 --keepdb
```

- If tests fail because of missing environment variables (e.g., `SECRET_KEY`), create a local `.env` from `.env.example` and export the values in your shell or CI secrets.

Writing new tests

- Add tests when fixing bugs or adding features. Aim to cover model logic, view behavior, form validation, and key templates.
- Use factories (e.g., Factory Boy) or fixtures to build test data where helpful.

CI recommendations

- Add a workflow that installs dependencies, runs `python manage.py check --deploy` with production-like env vars, and then runs `python manage.py test`.
- Consider splitting unit tests (fast) and integration tests (slow) into separate CI jobs.


## 🚀 Production Deployment

This project is configured for deployment using either Docker or Vercel.

### Option 1: Deploying with Docker

This is the recommended method for a full production-like environment with Nginx and PostgreSQL.

#### Prerequisites

*   Docker
*   Docker Compose

#### 1. Configure Environment

Create a `.env` file in the project root and add the following variables:

```
DEBUG=False
SECRET_KEY=<your-strong-secret-key>
```
The `DATABASE_URL` is already configured in `docker-compose.yml` to connect to the PostgreSQL service.

#### 2. Build and Run the Containers

```bash
docker-compose up -d --build
```

This command will build the Docker image for the web service, and start the `web`, `db` (PostgreSQL), and `nginx` services in detached mode.

#### 3. Accessing the Application

The application will be available at `http://localhost`. Nginx is configured to listen on port 80.

### Option 2: Deploying to Render

This project is configured for deployment on Render.com.

#### Prerequisites

*   A Render account
*   PostgreSQL database service on Render (or external PostgreSQL database)

#### 1. Configure Environment Variables

In your Render project settings, add the following environment variables:
*   `SECRET_KEY`: Your production secret key
*   `DEBUG`: Set to `False`
*   `USE_POSTGRES`: Set to `True`
*   `DATABASE_URL`: Your PostgreSQL connection string
*   Add other environment variables from `.env.example` as needed

#### 2. Deploy

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select the repository and branch
4. Configure build settings:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn gda.wsgi:application --bind 0.0.0.0:$PORT`

Render will automatically handle the deployment process. The current live demo is hosted on Render at [https://gda-oy5s.onrender.com](https://gda-oy5s.onrender.com)

### Option 3: Manual Deployment with WSGI/ASGI

For a more traditional deployment on a virtual machine or a bare-metal server, you can use a production-grade WSGI or ASGI server.

#### WSGI Deployment (e.g., with Gunicorn)

Gunicorn is a mature and widely used WSGI server for Unix-like systems.

```bash
# Install Gunicorn
pip install gunicorn

# Run the application with Gunicorn
gunicorn gda.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

On Windows, you can use `waitress`:
```bash
# Install Waitress
pip install waitress

# Run the application with Waitress
waitress-serve --listen=0.0.0.0:8000 gda.wsgi:application
```

#### ASGI Deployment (e.g., with Uvicorn)

If your application has asynchronous features (like Django Channels), you should use an ASGI server like Uvicorn.

```bash
# Install Uvicorn
pip install uvicorn

# Run the application with Uvicorn
uvicorn gda.asgi:application --host 0.0.0.0 --port 8000 --workers 4
```
## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for detailed information.

### Development Workflow
```mermaid
flowchart LR
    A[Fork Repository] --> B[Create Feature Branch]
    B --> C[Make Changes]
    C --> D[Write Tests]
    D --> E[Run Test Suite]
    E --> F[Submit Pull Request]
    F --> G[Code Review]
    G --> H[Merge to Main]
```

### Code Standards
- **PEP 8**: Python style guide compliance
- **Django Best Practices**: Framework-specific conventions
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Minimum 80% code coverage

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Global Development Alliance

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👥 Support

### Getting Help
- 📧 **Email**: anuragshankarmaurya@gmail.com
- 💬 **GitHub Discussions**: [Join the conversation](https://github.com/Anurag-Shankar-Maurya/GDA/discussions)
- 📖 **Wiki**: [Project Wiki](https://github.com/Anurag-Shankar-Maurya/GDA/wiki)
- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/Anurag-Shankar-Maurya/GDA/issues)

### Support Options
- **Community Support**: GitHub issues and discussions
- **Bug Reports**: Submit via GitHub Issues
- **Feature Requests**: Submit via GitHub Discussions
- **Security Issues**: Send directly to anuragshankarmaurya@gmail.com

## 🙏 Acknowledgments

### Core Team
- **Lead Developer**: [Anurag Shankar Maurya](https://github.com/Anurag-Shankar-Maurya)
- **Contributors**: Open source community members
- **Testers**: Community beta testers

### Technology Stack
- [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines
- [Bootstrap](https://getbootstrap.com/): The world's most popular frontend toolkit
- [Chart.js](https://www.chartjs.org/): Simple yet flexible JavaScript charting
- [PostgreSQL](https://www.postgresql.org/): The world's most advanced open source database
- [Docker](https://www.docker.com/): Containerization platform

### Special Thanks
To the open source community and all contributors who help make this project better.

---

<div align="center">

**Built with ❤️ by [Anurag Shankar Maurya](https://github.com/Anurag-Shankar-Maurya)**

[![GitHub stars](https://img.shields.io/github/stars/Anurag-Shankar-Maurya/GDA.svg?style=social&label=Star)](https://github.com/Anurag-Shankar-Maurya/GDA)
[![GitHub forks](https://img.shields.io/github/forks/Anurag-Shankar-Maurya/GDA.svg?style=social&label=Fork)](https://github.com/Anurag-Shankar-Maurya/GDA)

*Empowering volunteer organizations through technology*

</div>
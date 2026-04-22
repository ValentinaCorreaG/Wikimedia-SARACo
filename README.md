# Wikimedia Colombia SARA

A Django web application for Wikimedia Colombia with Wikimedia OAuth authentication, HTMX interactions, and a Tailwind CSS UI, deployed on Toolforge.

## ✨ Features

- 🔐 Wikimedia OAuth Authentication via social-auth-app-django
- 🎨 Modern UI with Tailwind CSS + DaisyUI
- ⚡ HTMX Integration for dynamic server-rendered interactions
- 🛡️ Production Security Settings (secure cookies, HTTPS-aware setup, CSRF hardening)
- 🧾 Application and Auth Logging with rotating files
- 📱 Responsive Interface
- 👤 User and Profile Management

## 🚀 Tech Stack

- **Backend**: Django 5.2.x+
- **Frontend**: HTMX + Tailwind CSS + DaisyUI
- **Authentication**: Python Social Auth (Wikimedia OAuth)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Static files**: WhiteNoise + collectstatic

## 📋 Prerequisites

- Python 3.10+ (Toolforge runtime example uses python3.13)
- Node.js + npm (for Tailwind CSS compilation)
- Wikimedia account (for OAuth consumer registration)

## 🔧 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd wikimedia-colombia-sara

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python manage.py tailwind install
python manage.py migrate
```

### 2. Configure environment variables

This project loads .env from project root on startup (without overriding existing OS env vars).
Create .env with values that match the current settings.py keys:

```bash
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
MEDIAWIKI_OAUTH_KEY=<consumer-key>
SOCIAL_AUTH_MEDIAWIKI_SECRET=<consumer-secret>
MEDIAWIKI_URL=https://meta.wikimedia.org/w/index.php
SOCIAL_AUTH_MEDIAWIKI_CALLBACK=http://127.0.0.1:8000/oauth/complete/mediawiki/
NPM_BIN_PATH=<path-to-npm>
```
Examples for NPM_BIN_PATH:

* Linux/macOS: NPM_BIN_PATH=$(command -v npm)
* Windows PowerShell: NPM_BIN_PATH=(Get-Command npm).Source

### 3. Run Development Servers

**Terminal 1 - Tailwind CSS:**
```bash
python manage.py tailwind start
```

**Terminal 2 - Django:**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

# 4. 🎨 Tailwind and static assets

In development, use tailwind start watcher.

For production:

```bash
python manage.py tailwind build
python manage.py collectstatic --noinput
```
If CSS requests return HTML (MIME error), static files were not built/collected correctly or the file does not exist in collected static output.

## 📁 Project Structure

```
Wikimedia-SARACo/
├── app.py
├── core/
├── users/
├── theme/
│   ├── static/
│   └── static_src/
├── wikimediacolombiasara/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```
app.py exposes app = get_wsgi_application() for Toolforge runtime compatibility.

## 🔐 Authentication Features

### Implemented High-Priority Improvements

✅ **Session Security**
- Secure cookies (HTTPS only in production)
- HTTPOnly and SameSite protection
- 24-hour session timeout

✅ **Comprehensive Logging**
- Authentication event logging
- Rotating log files (10MB, 5 backups)
- Separate auth and general logs

✅ **Error Handling**
- User-friendly error messages
- Detailed admin logging
- HTMX-aware responses

✅ **Testing**
- Pipeline function tests
- View permission tests
- HTMX integration tests
- Model creation tests

### Authentication Flow

1. User clicks "Sign in with Wikimedia"
2. OAuth redirect to Wikimedia
3. User authorizes application
4. Custom pipeline:
   - Matches existing users by wiki handle
   - Resolves username conflicts
   - Creates user profile automatically
   - Logs authentication event
5. User redirected to home page

## 🎨 UI Components

### HTMX Features
- Partial page updates
- Smooth transitions
- Progressive enhancement
- No full page reloads

```bash
python manage.py collectstatic
```

### Templates
- `theme/templates/base.html` - Base layout with messages
- `theme/templates/partials/sidebar.html` - Navigation
- `users/templates/users/` - Authentication templates

## 🚀 Production Deployment

### Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up log rotation
- [ ] Monitor authentication logs
- [ ] Build Tailwind for production: `python manage.py tailwind build`
- [ ] Collect static files: `python manage.py collectstatic`

### Environment Variables

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<strong-random-key>
DJANGO_ALLOWED_HOSTS=yourdomain.com
MEDIAWIKI_OAUTH_KEY=<production-key>
MEDIAWIKI_OAUTH_SECRET=<production-secret>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python manage.py test`
5. Submit a pull request


## 🎯 Toolforge Deployment

The application was deployed on Toolforge, following the official deployment documentation (https://wikitech.wikimedia.org/wiki/Help:Toolforge/My_first_Django_OAuth_tool#Configure_project_for_production_environment__) and best practices for hosting Wikimedia-related tools.

🌐 Live Tool
Visit `https://sara-colombia.toolforge.org/`

---

Built with ❤️ for Wikimedia Colombia

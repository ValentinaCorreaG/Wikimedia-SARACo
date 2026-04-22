# Wikimedia Colombia SARA

A modern Django web application with Wikimedia OAuth authentication, built with HTMX and Tailwind CSS.

## ✨ Features

- 🔐 **Wikimedia OAuth Authentication** - Secure login with Wikimedia accounts
- 🎨 **Modern UI** - Beautiful interface with Tailwind CSS and DaisyUI
- ⚡ **HTMX Integration** - Dynamic interactions without heavy JavaScript
- 🛡️ **Security First** - Session security, logging, and best practices
- 📱 **Responsive Design** - Mobile-first approach
- 🧪 **Comprehensive Tests** - Full test coverage for authentication
- 📊 **User Management** - Profiles, teams, and positions

## 🚀 Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTMX + Tailwind CSS + DaisyUI
- **Authentication**: Python Social Auth (Wikimedia OAuth)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Testing**: Django Test Framework

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+ (for Tailwind CSS compilation)
- npm or yarn
- A Wikimedia account (for OAuth setup)

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
```

### 2. Configure OAuth

1. Register your app at [Wikimedia OAuth](https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration)
2. Copy `.env.example` to `.env`
3. Add your OAuth credentials to `.env`

See [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) for detailed instructions.

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### 4. Run Development Servers

**Terminal 1 - Tailwind CSS:**
```bash
python manage.py tailwind start
```

**Terminal 2 - Django:**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## 📁 Project Structure

```
wikimedia-colombia-sara/
├── core/                      # Main application
├── users/                     # Authentication & user management
│   ├── models.py             # User, UserProfile, TeamArea, Position
│   ├── views.py              # Authentication views
│   ├── pipeline.py           # Custom OAuth pipeline
│   ├── tests.py              # Comprehensive test suite
│   ├── templates/            # User templates
│   │   └── users/
│   │       ├── login.html
│   │       ├── profile.html
│   │       └── partials/     # HTMX partials
│   └── urls.py
├── theme/                     # Tailwind CSS app
│   ├── static/
│   │   └── css/dist/         # Compiled CSS
│   ├── static_src/           # Source files
│   │   ├── src/styles.css
│   │   └── tailwind.config.js
│   └── templates/
│       ├── base.html
│       └── partials/
│           └── sidebar.html
├── wikimediacolombiasara/    # Django settings
│   ├── settings.py           # With security & logging
│   └── urls.py
├── logs/                      # Application logs
├── .env.example              # Environment template
├── requirements.txt
├── AUTHENTICATION_SETUP.md   # Detailed auth guide
└── README.md
```

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

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run authentication tests only
python manage.py test users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

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

## 📝 License

[Add your license here]

## 🆘 Support

- Check `logs/` directory for application logs
- Review [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) for OAuth issues
- Check Django debug page in development
- Review test suite for usage examples

## 🎯 Deployment

You can access the tool at https://sara-colombia.toolforge.org/

The application was deployed on Toolforge, following the official deployment documentation (https://wikitech.wikimedia.org/wiki/Help:Toolforge/My_first_Django_OAuth_tool#Configure_project_for_production_environment__) and best practices for hosting Wikimedia-related tools.

---

Built with ❤️ for Wikimedia Colombia

# Django REST API - Task Management System

A robust RESTful API built with Django and Django REST Framework, following best practices of layered architecture with separation between selectors (read) and services (write).

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Installation and Setup](#installation-and-setup)
- [How the Project Works](#how-the-project-works)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [CI/CD - Continuous Integration](#cicd---continuous-integration)
- [Deployment](#deployment)

## ✨ Features

- **Complete RESTful API** with Django REST Framework
- **Authentication** via Session and Token Authentication
- **Custom User Model** extending AbstractUser
- **Configurable pagination** for listings
- **Layered architecture** (Views → Services/Selectors → Models)
- **Multiple environments** (dev, prod) with separate configurations
- **Automatic timestamps** on all models via TimeStampedModel
- **Automated tests** to ensure code quality
- **Django Admin** for internal management

## 🛠️ Technologies Used

- **Python 3.x**
- **Django 5.2**
- **Django REST Framework** - For creating the REST API
- **SQLite** - Database in development
- **Django Debug Toolbar** - Debug tools in development

## 🏗️ Project Architecture

This project follows a layered architecture inspired by DDD (Domain-Driven Design):

### Application Layers

```
┌─────────────────────────────────────┐
│         API Layer (Views)           │
│     - Receives HTTP requests        │
│     - Validates data (Serializers)  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────┴───────────────────┐
│      Business Logic Layer           │
├─────────────────┬───────────────────┤
│   Services      │    Selectors      │
│   (Write)       │    (Read)         │
│ - create_task   │ - list_tasks      │
│ - update_task   │ - get_task        │
│ - delete_task   │                   │
└─────────────────┴───────────────────┘
                  │
┌─────────────────┴───────────────────┐
│         Data Layer (Models)         │
│     - Defines data structure        │
│     - Interacts with database       │
└─────────────────────────────────────┘
```

### Separation Pattern: Selectors vs Services

- **Selectors** (`selectors.py`): Read functions (queries). Return QuerySets or database objects.
- **Services** (`services.py`): Write functions (commands). Encapsulate business logic for create/update/delete.

**Advantages:**
- More testable and organized code
- Business logic isolated from views
- Easy code reusability
- Facilitates future refactoring

## 📁 Directory Structure

```
django-api/
├── config/                         # Django project configurations
│   ├── settings/
│   │   ├── base.py                 # Shared base configurations
│   │   ├── dev.py                  # Development configurations
│   │   └── prod.py                 # Production configurations
│   ├── urls.py                     # Main project URLs
│   ├── wsgi.py                     # WSGI configuration
│   └── asgi.py                     # ASGI configuration
│
├── core/                           # Central app with shared code
│   ├── models.py                   # TimeStampedModel (abstract base model)
│   └── pagination.py               # Custom pagination class
│
├── users/                          # Users app
│   ├── models.py                   # Custom User model
│   └── api/
│       ├── views.py                # UserViewSet (ReadOnly for admins)
│       ├── serializers.py          # UserSerializer
│       └── urls.py                 # User routes
│
├── tasks/                          # Tasks app
│   ├── models.py                   # Task model
│   ├── selectors.py                # Query functions (read)
│   ├── services.py                 # Business functions (write)
│   ├── api/
│   │   ├── views.py                # TaskViewSet
│   │   ├── serializers.py          # TaskSerializer
│   │   └── urls.py                 # Task routes
│   └── tests/
│       └── test_tasks_api.py       # Task API tests
│
├── manage.py                       # Django CLI
├── db.sqlite3                      # SQLite database
└── README.md                       # This file
```

## 🚀 Installation and Setup

### Option 1: Using Dev Container (Recommended) 🐳

The easiest way to get started is using the Dev Container, which provides a pre-configured development environment with all dependencies.

**Prerequisites:**
- Docker Desktop installed and running
- VS Code or Cursor with the "Dev Containers" extension

**Quick Start:**
1. Open the project in VS Code/Cursor
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type: `Dev Containers: Reopen in Container`
4. Wait for the container to build (first time: ~5-10 minutes)

**What Gets Configured Automatically:**

The container automatically sets up:
- ✅ Python 3.12 with all dependencies
- ✅ Database migrations applied
- ✅ Default superuser created (`admin` / `admin`)
- ✅ Git hooks for code quality checks
- ✅ SSH keys mounted from host (read-only)
- ✅ VS Code extensions (Python, Black, isort, Ruff)

**Access Points:**
- **API**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin (login: `admin` / `admin`)
- **Dev Server**: Start with `make run` or `python manage.py runserver 0.0.0.0:8000`

**🔑 SSH Configuration:**

The dev container automatically mounts your SSH configuration from the host machine, enabling:
- Push/pull from private Git repositories
- SSH authentication for GitHub, GitLab, Bitbucket, etc.
- Secure key storage on host (read-only mount)

Test SSH inside the container:
```bash
ssh -T git@github.com
```

**🔧 Common Troubleshooting:**

| Issue | Solution |
|-------|----------|
| Container won't start | Rebuild with `F1` → "Dev Containers: Rebuild Container" |
| Port 8000 in use | Stop other processes or change port in `docker-compose.yml` |
| Dependencies not found | Run `pip install -r requirements.txt requirements-dev.txt` |
| SSH keys not working | Verify `~/.ssh` exists on host, check [.devcontainer/SSH_SETUP.md](.devcontainer/SSH_SETUP.md) |

**📚 Detailed Documentation:**
- Full setup guide: [.devcontainer/README.md](.devcontainer/README.md)
- SSH configuration: [.devcontainer/SSH_SETUP.md](.devcontainer/SSH_SETUP.md)

---

### Option 2: Manual Installation

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/lucas54neves/django-api.git
cd django-api
```

### Step 2: Create and Activate Virtual Environment

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Or install packages manually:**
```bash
pip install django djangorestframework django-debug-toolbar
```

### Step 4: Configure Environment Variables (Optional)

For production, set the `DJANGO_SECRET_KEY` variable:

```bash
export DJANGO_SECRET_KEY='your-secret-key-here'
```

### Step 5: Run Migrations

```bash
python manage.py migrate
```

### Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the instructions to create username, email, and password.

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## 🔍 How the Project Works

### 1. Environment-Based Configuration

The project uses multiple configuration files:

- **`base.py`**: Common settings (installed apps, middleware, base database)
- **`dev.py`**: Inherits from `base.py` and adds DEBUG=True, debug_toolbar
- **`prod.py`**: Inherits from `base.py` with DEBUG=False and production settings

The `manage.py` file is configured to use `config.settings.dev` by default.

### 2. Custom User Model

The project uses a custom user model (`users.User`) that inherits from `AbstractUser`:

```python
# users/models.py
class User(AbstractUser, TimeStampedModel):
    pass  # Add extra fields as needed
```

Defined in `base.py`:
```python
AUTH_USER_MODEL = 'users.User'
```

**⚠️ Important:** The custom user must be defined before running the first migration.

### 3. TimeStampedModel - Abstract Base Model

All models inherit from `TimeStampedModel` to have automatic timestamp fields:

```python
# core/models.py
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

### 4. Task Model

```python
# tasks/models.py
class Task(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
```

Each task belongs to a user (owner) and has a title and completion status.

### 5. Services and Selectors Architecture

**Selectors** (queries):
```python
# tasks/selectors.py
def list_tasks_for_user(user):
    return Task.objects.filter(owner=user).order_by('-created_at')

def get_task_for_user(*, user, task_id: int):
    return Task.objects.filter(owner=user, id=task_id).first()
```

**Services** (write operations):
```python
# tasks/services.py
def create_task(*, owner, title: str, done: bool = False) -> Task:
    return Task.objects.create(owner=owner, title=title, done=done)

def update_task(*, task: Task, **data) -> Task:
    for field, value in data.items():
        setattr(task, field, value)
    task.save()
    return task

def delete_task(*, task: Task):
    task.delete()
```

**ViewSet using services and selectors:**
```python
# tasks/api/views.py
class TaskViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return selectors.list_tasks_for_user(self.request.user)
    
    def perform_create(self, serializer):
        task = services.create_task(
            owner=self.request.user,
            title=serializer.validated_data['title'],
            done=serializer.validated_data.get('done', False),
        )
        serializer.instance = task
```

### 6. Authentication and Permissions

Configured in `base.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

- All routes require authentication by default
- Supports authentication via Session (for browser) and Token (for apps)

### 7. URL Routing

Main URLs (`config/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('users.api.urls')),
        path('', include('tasks.api.urls')),
    ])),
]
```

Task routes (`tasks/api/urls.py`):
```python
router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
urlpatterns = router.urls
```

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication

To access the API, you need to be authenticated. Use Django Admin to login:

1. Access `http://localhost:8000/admin/`
2. Login with the created superuser
3. Use Session Authentication or configure Token Authentication

### Task Endpoints

#### List all tasks for authenticated user
```http
GET /api/v1/tasks/
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "My first task",
      "done": false,
      "created_at": "2025-11-27T10:30:00Z",
      "updated_at": "2025-11-27T10:30:00Z"
    }
  ]
}
```

#### Create new task
```http
POST /api/v1/tasks/
Content-Type: application/json

{
  "title": "New task",
  "done": false
}
```

#### Get task details
```http
GET /api/v1/tasks/{id}/
```

#### Update task
```http
PUT /api/v1/tasks/{id}/
Content-Type: application/json

{
  "title": "Updated task",
  "done": true
}
```

#### Partial update
```http
PATCH /api/v1/tasks/{id}/
Content-Type: application/json

{
  "done": true
}
```

#### Delete task
```http
DELETE /api/v1/tasks/{id}/
```

### User Endpoints (Admin Only)

#### List users
```http
GET /api/v1/users/
```

#### User details
```http
GET /api/v1/users/{id}/
```

**Note:** Only admin users can access user endpoints.

### Pagination

The API uses pagination by default:

- **Default page size:** 20 items
- **Maximum size:** 100 items
- **Custom parameter:** `?page_size=50`

Example:
```http
GET /api/v1/tasks/?page=2&page_size=10
```

## 🧪 Testing

The project includes automated tests for the task API.

### Quick Start with Makefile

The project includes a Makefile with convenient commands for development:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install production dependencies |
| `make install-dev` | Install development dependencies (linters, test tools) |
| `make test` | Run all tests |
| `make test-coverage` | Run tests with coverage report |
| `make lint` | Run all linting checks (Black, isort, Flake8, Pylint) |
| `make format` | Auto-format code (Black + isort) |
| `make check` | Run lint + tests (same as CI pipeline) |
| `make clean` | Remove temporary files and caches |
| `make run` | Start development server |
| `make migrate` | Run database migrations |
| `make makemigrations` | Create new migrations |
| `make shell` | Open Django shell |

**Recommended Development Workflow:**

```bash
# 1. Format code automatically
make format

# 2. Run all checks (same as CI)
make check

# 3. If everything passes, commit
git add .
git commit -m "feat: new feature"
git push
```

### Run Tests Manually

**Run all tests:**
```bash
python manage.py test
```

**Run tests for a specific app:**
```bash
python manage.py test tasks
```

**Run with verbosity:**
```bash
python manage.py test --verbosity=2
```

**Run with coverage:**
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report in htmlcov/
```

### Code Quality and Linting

The project uses multiple tools to ensure code quality:

**Black** (code formatting):
```bash
black .
# Configuration in pyproject.toml: line-length = 127
```

**isort** (import organization):
```bash
isort .
# Configuration in pyproject.toml: profile = "black"
```

**Flake8** (style guide enforcement):
```bash
flake8 .
# Configuration in .flake8: max-line-length = 127, max-complexity = 10
```

**Pylint** (code analysis):
```bash
pylint --disable=all --enable=E,F --ignore=migrations,venv **/*.py
# Configuration in pyproject.toml: Focuses on errors (E) and fatal issues (F)
```

**Configuration Files:**

- `.flake8` - Flake8 settings (line length, exclusions, complexity)
- `pyproject.toml` - Black, isort, Pylint, and Coverage settings

**Best Practices:**

✅ Run `make format` before committing  
✅ Run `make check` to validate (same as CI)  
✅ Keep test coverage above 80%  
✅ Write tests for new features  
✅ Use Git hooks for automatic validation  
✅ Review CI logs when builds fail

### Test Structure

Tests are in `tasks/tests/test_tasks_api.py` and cover:

- Task creation
- Task listing
- Task updates
- Task deletion
- Permissions and isolation between users

## 🔄 CI/CD - Continuous Integration

The project includes a GitHub Actions workflow that automatically runs on every push or pull request to the `main` branch.

### What the CI Pipeline Does

The workflow (`.github/workflows/ci.yml`) automatically:

1. **✅ Code Formatting Check** - Validates code formatting with Black
2. **✅ Import Organization** - Checks import sorting with isort
3. **✅ Code Linting** - Runs Flake8 and Pylint to catch errors and style issues
4. **✅ All Tests** - Executes the complete test suite
5. **✅ Coverage Report** - Generates test coverage reports
6. **✅ Multi-Python Version** - Tests on Python 3.11 and 3.12

### Workflow Triggers

The CI runs automatically on:
- ✅ Push to `main` branch
- ✅ Pull requests targeting `main` branch

### Tools and Configuration

The project uses multiple tools to ensure code quality:

| Tool | Purpose | Configuration File |
|------|---------|-------------------|
| **Black** | Code formatting (PEP 8) | `pyproject.toml` |
| **isort** | Import organization | `pyproject.toml` |
| **Flake8** | Style guide enforcement | `.flake8` |
| **Pylint** | Static code analysis | `pyproject.toml` |
| **pytest** | Testing framework | `pyproject.toml` |
| **Coverage** | Code coverage tracking | `pyproject.toml` |

### Running CI Checks Locally

Before pushing code, run the same checks locally to avoid CI failures:

```bash
# Run everything (lint + tests) - same as CI
make check

# Or run individually
make format        # Auto-fix formatting (Black + isort)
make lint          # All linting checks
make test          # All tests
make test-coverage # Tests with coverage report
```

### Git Hooks (Optional but Recommended)

Configure Git hooks to run checks automatically before each commit:

```bash
# Make the script executable
chmod +x setup_hooks.sh

# Run the setup script
./setup_hooks.sh
```

This configures pre-commit hooks that prevent committing code with formatting or linting issues.

### Viewing CI Results

1. Go to your GitHub repository
2. Click on **"Actions"** tab
3. Select **"CI - Lint and Tests"** workflow
4. Click on a specific run to see detailed logs
5. Download coverage reports from artifacts (available for 30 days)

**Add a CI Status Badge to README:**

```markdown
![CI Status](https://github.com/YOUR-USERNAME/YOUR-REPO/workflows/CI%20-%20Lint%20and%20Tests/badge.svg)
```

### Branch Protection (Recommended)

Configure branch protection to prevent merging code with issues:

1. Go to **Settings** → **Branches** on GitHub
2. Click **Add rule**
3. Branch name pattern: `main`
4. Enable:
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
5. Select the check: **lint-and-test**
6. Save changes

This ensures PRs with failing tests or linting issues cannot be merged.

### CI/CD Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| ❌ "Black would reformat" | Code not formatted | Run `make format` |
| ❌ "isort would reformat" | Imports disorganized | Run `make format` |
| ❌ "Flake8 found errors" | Style violations | Run `flake8 .` and fix issues |
| ❌ "Tests failed" | Test failures | Run `make test` locally and fix |
| ❌ Workflow doesn't run | Actions disabled | Check Settings → Actions |

### Development Dependencies

Install all linting and testing tools:

```bash
# Install dev dependencies
make install-dev

# Or manually
pip install -r requirements-dev.txt
```

**Included tools:**
- **black** (code formatter)
- **isort** (import sorter)
- **flake8** (style guide enforcer)
- **pylint** (code analyzer)
- **pytest** & **pytest-django** (testing)
- **coverage** (coverage tracking)

### Detailed Workflow Documentation

For advanced workflow configuration and customization, see:
- [.github/workflows/README.md](.github/workflows/README.md) - Detailed workflow documentation
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - Workflow configuration file

## 🚀 Deployment

### Production Preparation

1. **Change environment to production:**

   Edit `wsgi.py` or set the environment variable:
   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
   ```

2. **Configure SECRET_KEY:**

   ```bash
   export DJANGO_SECRET_KEY='super-secure-secret-key'
   ```

3. **Configure database (PostgreSQL recommended):**

   In `config/settings/prod.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Configure ALLOWED_HOSTS:**

   ```python
   ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
   ```

5. **Collect static files:**

   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

### Deployment Options

- **Heroku**: Easy platform for Django application deployment
- **AWS EC2**: Configurable virtual machines
- **DigitalOcean**: Droplets with simplified configuration
- **Railway**: Modern and simplified deployment
- **Render**: Modern alternative to Heroku

### WSGI/ASGI Server

For production, use servers like:

- **Gunicorn** (WSGI)
  ```bash
  pip install gunicorn
  gunicorn config.wsgi:application --bind 0.0.0.0:8000
  ```

- **Uvicorn** (ASGI)
  ```bash
  pip install uvicorn
  uvicorn config.asgi:application --host 0.0.0.0 --port 8000
  ```

### Nginx as Reverse Proxy

Configure Nginx to serve the application:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

## 📝 Implemented Best Practices

✅ Separation of configurations by environment  
✅ Custom user model  
✅ Layered architecture (Services/Selectors)  
✅ Use of keyword-only arguments (`*`) in functions  
✅ Configurable pagination  
✅ Required authentication  
✅ Automatic timestamps  
✅ Automated tests  
✅ Data isolation per user  

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/MyFeature`)
3. Commit your changes (`git commit -m 'Add MyFeature'`)
4. Push to the branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact

Lucas Neves - [@lucas54neves](https://github.com/lucas54neves)

---

**Developed with ❤️ using Django and Django REST Framework**

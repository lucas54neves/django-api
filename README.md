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
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      Business Logic Layer           │
├─────────────────┬───────────────────┤
│   Services      │    Selectors      │
│   (Write)       │    (Read)         │
│ - create_task   │ - list_tasks      │
│ - update_task   │ - get_task        │
│ - delete_task   │                   │
└─────────────────┴───────────────────┘
               │
┌──────────────┴──────────────────────┐
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
├── config/                      # Django project configurations
│   ├── settings/
│   │   ├── base.py             # Shared base configurations
│   │   ├── dev.py              # Development configurations
│   │   └── prod.py             # Production configurations
│   ├── urls.py                 # Main project URLs
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
│
├── core/                        # Central app with shared code
│   ├── models.py               # TimeStampedModel (abstract base model)
│   └── pagination.py           # Custom pagination class
│
├── users/                       # Users app
│   ├── models.py               # Custom User model
│   └── api/
│       ├── views.py            # UserViewSet (ReadOnly for admins)
│       ├── serializers.py      # UserSerializer
│       └── urls.py             # User routes
│
├── tasks/                       # Tasks app
│   ├── models.py               # Task model
│   ├── selectors.py            # Query functions (read)
│   ├── services.py             # Business functions (write)
│   ├── api/
│   │   ├── views.py            # TaskViewSet
│   │   ├── serializers.py      # TaskSerializer
│   │   └── urls.py             # Task routes
│   └── tests/
│       └── test_tasks_api.py   # Task API tests
│
├── manage.py                    # Django CLI
├── db.sqlite3                   # SQLite database
└── README.md                    # This file
```

## 🚀 Installation and Setup

### Prerequisites

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

### Run all tests

```bash
python manage.py test
```

### Run tests for a specific app

```bash
python manage.py test tasks
```

### Run with verbosity

```bash
python manage.py test --verbosity=2
```

### Test Structure

Tests are in `tasks/tests/test_tasks_api.py` and cover:

- Task creation
- Task listing
- Task updates
- Task deletion
- Permissions and isolation between users

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

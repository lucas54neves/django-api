# Dev Container Configuration

This directory contains the configuration for developing this Django project inside a Docker container using VS Code or Cursor's Dev Containers feature.

## 🎯 What's Included

### Container Features

- **Python 3.12** with all project dependencies pre-installed
- **Git** and **GitHub CLI** for version control
- **SQLite** database ready to use
- **Django development server** configured
- **VS Code extensions** for Python development:
  - Python, Pylance (IntelliSense)
  - Black (code formatter)
  - isort (import sorter)
  - Ruff (fast linter)
  - Docker extension
  - GitLens and Git Graph

### Automatic Setup

When the container starts, it automatically:

1. ✅ Installs all Python dependencies
2. ✅ Runs database migrations
3. ✅ Creates a default superuser (`admin` / `admin`)
4. ✅ Sets up Git hooks for code quality
5. ✅ Configures SSH keys from your host machine

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop** installed and running
- **VS Code** or **Cursor** with "Dev Containers" extension

### How to Open

1. Open the project folder in VS Code/Cursor
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **"Dev Containers: Reopen in Container"**
4. Wait for the container to build (first time takes ~5-10 minutes)

### Access the Application

Once the container is running:

- **Django Dev Server**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
  - Username: `admin`
  - Password: `admin`
- **API Endpoints**: http://localhost:8000/api/v1/

### Start the Development Server

Open a terminal in VS Code/Cursor and run:

```bash
python manage.py runserver 0.0.0.0:8000
```

## 📂 File Structure

```
.devcontainer/
├── devcontainer.json       # Main configuration
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Docker Compose configuration
├── postCreateCommand.sh    # Setup script (runs after container creation)
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔧 Configuration Details

### Python Environment

- **Interpreter**: `/usr/local/bin/python`
- **Virtual environment**: Not needed (isolated container)
- **Dependencies**: Installed from `requirements.txt` and `requirements-dev.txt`

### VS Code Settings

The container automatically configures:

- **Black** as the default Python formatter
- **isort** for import organization
- **Format on save** enabled
- **Pylint** and **Flake8** for linting
- **Pytest** for running tests

### SSH Configuration

Your SSH keys from `~/.ssh` on the host machine are automatically mounted into the container (read-only). This allows you to:

- Push/pull from private Git repositories
- Use SSH authentication with GitHub, GitLab, etc.
- Keep your keys secure on the host

Test SSH inside the container:

```bash
ssh -T git@github.com
```

## 🛠️ Development Workflow

### Running Commands

All commands run inside the container. Open a terminal in VS Code/Cursor:

```bash
# Database operations
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser

# Run tests
make test
make test-coverage

# Code quality
make lint
make format

# Django shell
python manage.py shell

# Start dev server
python manage.py runserver 0.0.0.0:8000
```

### Making Changes

1. Edit code normally in VS Code/Cursor
2. Changes are synced immediately (volume mount)
3. Django dev server auto-reloads on file changes
4. Linting and formatting happen automatically on save

### Debugging

The Python extension is configured for debugging:

1. Set breakpoints in your code
2. Press `F5` or use "Run and Debug" panel
3. Select "Python: Django" configuration

## 🔍 Troubleshooting

### Container Won't Start

**Check Docker Desktop is running:**

```bash
docker ps
```

**Rebuild the container:**

1. Press `F1` → "Dev Containers: Rebuild Container"
2. Or run: `docker-compose -f .devcontainer/docker-compose.yml build --no-cache`

### Port 8000 Already in Use

Stop any processes using port 8000:

```bash
# Find process
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>
```

Or change the port in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Use 8001 on host instead
```

### SSH Keys Not Working

**Verify SSH mount:**

```bash
# Inside container
ls -la ~/.ssh
```

**Check permissions:**

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa  # or id_ed25519
```

**Test SSH connection:**

```bash
ssh -vT git@github.com
```

### Python Dependencies Not Found

**Reinstall dependencies:**

```bash
pip install --user -r requirements.txt
pip install --user -r requirements-dev.txt
```

### Database Issues

**Reset database:**

```bash
# Inside container
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🔄 Updating the Container

### After Changing Dependencies

If you modify `requirements.txt` or `requirements-dev.txt`:

1. Rebuild the container: `F1` → "Dev Containers: Rebuild Container"
2. Or manually: `pip install --user -r requirements.txt`

### After Changing Docker Files

If you modify `Dockerfile` or `docker-compose.yml`:

1. Rebuild from scratch: `F1` → "Dev Containers: Rebuild Container Without Cache"

## 📦 What Gets Installed

### Python Packages (Production)

From `requirements.txt`:
- Django 5.2
- djangorestframework
- django-debug-toolbar

### Python Packages (Development)

From `requirements-dev.txt`:
- black (code formatter)
- isort (import sorter)
- flake8 (linter)
- pylint (code analyzer)
- pytest & pytest-django (testing)
- coverage (code coverage)

### System Packages

- git
- curl
- build-essential
- libpq-dev (PostgreSQL client)
- sqlite3
- openssh-client

## 🌟 Best Practices

### Do's ✅

- Commit your work frequently
- Run `make lint` before committing
- Use `make format` to auto-format code
- Run `make test` to ensure tests pass
- Keep dependencies up to date

### Don'ts ❌

- Don't install packages globally (use `--user` flag)
- Don't commit `db.sqlite3` (it's gitignored)
- Don't modify files outside the workspace
- Don't run as root user

## 🆘 Getting Help

If you encounter issues:

1. Check this README for troubleshooting steps
2. Check Docker logs: `docker logs <container-id>`
3. Check VS Code output: "Dev Containers" panel
4. Rebuild container without cache
5. Open an issue on the project repository

## 📚 Additional Resources

- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)

---

**Happy Coding! 🚀**

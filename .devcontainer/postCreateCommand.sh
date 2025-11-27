#!/bin/bash
# Post-create script: runs once after the container is created
set -e

echo "🚀 Starting post-create setup..."

# Ensure we're in the workspace directory
cd /workspace

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --user -r requirements.txt
if [ -f requirements-dev.txt ]; then
    pip install --user -r requirements-dev.txt
fi

# Fix SSH permissions if mounted (SSH keys are read-only)
if [ -d "$HOME/.ssh" ]; then
    echo "🔑 Fixing SSH permissions..."
    # Check if we have any keys
    if [ -f "$HOME/.ssh/id_rsa" ] || [ -f "$HOME/.ssh/id_ed25519" ]; then
        # SSH is read-only mounted, so we create a writable copy if needed
        mkdir -p "$HOME/.ssh-temp"
        cp -r "$HOME/.ssh"/* "$HOME/.ssh-temp/" 2>/dev/null || true
        chmod 700 "$HOME/.ssh-temp"
        find "$HOME/.ssh-temp" -type f -exec chmod 600 {} \;
        echo "  ✅ SSH keys available (writable copy at ~/.ssh-temp if needed)"
    fi
    # Configure git to use SSH for GitHub/GitLab
    if command -v git &> /dev/null; then
        git config --global --get url."git@github.com:".insteadOf > /dev/null 2>&1 || \
            git config --global url."git@github.com:".insteadOf "https://github.com/"
    fi
fi

# Run database migrations
if [ -f "manage.py" ]; then
    echo "🗄️  Running database migrations..."
    python manage.py migrate --no-input
    
    # Create default superuser for development
    echo "👤 Setting up default superuser..."
    python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('  ✅ Superuser created: username=admin, password=admin')
else:
    print('  ℹ️  Superuser already exists')
EOF
fi

# Set up Git hooks
if [ -f "setup_hooks.sh" ]; then
    echo "🪝 Setting up Git hooks..."
    chmod +x setup_hooks.sh
    bash setup_hooks.sh
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
fi

echo ""
echo "✅ Dev container setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Start the server: python manage.py runserver 0.0.0.0:8000"
echo "  2. Or use Makefile: make run (if available)"
echo ""
echo "🌐 Access points:"
echo "  • Django Dev Server: http://localhost:8000"
echo "  • Django Admin: http://localhost:8000/admin"
echo "  • API Endpoints: http://localhost:8000/api/v1/"
echo ""
echo "👤 Default credentials:"
echo "  • Username: admin"
echo "  • Password: admin"
echo ""
echo "🛠️  Useful commands:"
echo "  • make test          - Run tests"
echo "  • make lint          - Run linters"
echo "  • make format        - Format code"
echo "  • make check         - Run lint + tests (CI checks)"
echo ""
echo "🔑 SSH Configuration:"
echo "  • Your SSH keys are mounted from: ~/.ssh (read-only)"
echo "  • Test SSH: ssh -T git@github.com"
echo "  • For more details: cat .devcontainer/SSH_SETUP.md"
echo ""


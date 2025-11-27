#!/bin/bash
# Script to configure local Git hooks for code validation before commit

echo "🔧 Setting up Git hooks for the project..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create the pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook: runs checks before allowing commit

echo "🔍 Running code checks..."

# Check if we're in the correct directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: This hook must be run from the Django project root"
    exit 1
fi

# Flag to track if any errors occurred
ERRORS=0

# 1. Black - Formatting check
echo ""
echo "📝 Checking formatting with Black..."
if ! black --check --diff . --quiet; then
    echo "❌ Error: Code is not properly formatted"
    echo "💡 Run: make format or black ."
    ERRORS=1
fi

# 2. isort - Import check
echo ""
echo "📦 Checking import organization with isort..."
if ! isort --check-only . --quiet; then
    echo "❌ Error: Imports are not properly organized"
    echo "💡 Run: make format or isort ."
    ERRORS=1
fi

# 3. Flake8 - Linting
echo ""
echo "🐍 Running Flake8..."
if ! flake8 . --quiet; then
    echo "❌ Error: Flake8 found issues in the code"
    echo "💡 Run: flake8 . to see details"
    ERRORS=1
fi

# Final result
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed! Proceeding with commit..."
    exit 0
else
    echo "❌ Some checks failed. Commit blocked."
    echo ""
    echo "To automatically fix formatting issues:"
    echo "  make format"
    echo ""
    echo "To skip this hook (not recommended):"
    echo "  git commit --no-verify"
    exit 1
fi
EOF

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo ""
echo "✅ Git hooks configured successfully!"
echo ""
echo "📋 What was configured:"
echo "  - Pre-commit hook: Validates code before each commit"
echo "  - Checks formatting (Black)"
echo "  - Checks imports (isort)"
echo "  - Runs linting (Flake8)"
echo ""
echo "💡 Tip: Install development dependencies:"
echo "  make install-dev"
echo ""
echo "🚀 Now your commits will be validated automatically!"

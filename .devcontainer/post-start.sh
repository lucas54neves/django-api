#!/bin/bash
# Post-start script: runs every time the container starts

set -e

echo "🚀 Container started!"

# Test SSH connection (optional, non-blocking)
if command -v ssh &> /dev/null; then
    echo ""
    echo "🔑 Testing SSH connections..."
    
    # Test GitHub
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo "  ✅ GitHub SSH: Connected"
    else
        echo "  ⚠️  GitHub SSH: Not authenticated (this is normal if you don't use SSH)"
    fi
    
    # Note: Add more SSH tests here if needed
fi

echo ""
echo "✨ Ready for development!"
echo ""


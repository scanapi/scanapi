#!/bin/bash

# ScanAPI Development Environment Setup Script
# This script runs after the devcontainer is created

set -e

echo "🚀 Setting up ScanAPI development environment..."

# Update system packages
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y || true

# Install uv for faster dependency management
echo "📥 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Navigate to workspace
cd /workspaces/scanapi

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
$HOME/.cargo/bin/uv venv

# Activate virtual environment by setting PATH
export PATH="/workspaces/scanapi/.venv/bin:$PATH"
export VIRTUAL_ENV="/workspaces/scanapi/.venv"

# Install development dependencies with uv
echo "📚 Installing project dependencies with uv..."
$HOME/.cargo/bin/uv pip install -e ".[dev]"

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
uv run pre-commit install

# Clone examples repository for testing
echo "📚 Cloning ScanAPI examples for testing..."
cd /workspaces
if [ ! -d "examples" ]; then
  git clone https://github.com/scanapi/examples.git
  echo "✅ Examples cloned to /workspaces/examples"
else
  echo "✅ Examples already present"
fi

# Return to scanapi folder
cd /workspaces/scanapi

# Run initial checks to verify setup
echo "✅ Running initial checks..."
uv run ruff check . --select=E,W --show-fixes 2>/dev/null || true
uv run pytest --collect-only -q 2>/dev/null || true

echo ""
echo "✨ Setup complete! You're ready to develop ScanAPI."
echo ""
echo "📖 Quick commands:"
echo "  make test     - Run tests with coverage"
echo "  make lint     - Run linting with ruff"
echo "  make mypy     - Run type checking"
echo "  make check    - Run lint + mypy"
echo "  make format   - Format code with ruff"
echo ""
echo "🧪 Run tests:   uv run pytest tests/"
echo "📝 View docs:   cd documentation && make html"
echo ""

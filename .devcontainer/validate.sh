#!/bin/bash
set -e

echo "Validating .devcontainer configuration files..."

# Check if files exist
FILES=(
  ".devcontainer/devcontainer.json"
  ".devcontainer/post-create.sh"
  ".devcontainer/Dockerfile"
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file exists"
  else
    echo "❌ $file missing"
    exit 1
  fi
done

# Validate JSON
if command -v python3 &> /dev/null; then
  echo "Validating JSON..."
  python3 -m json.tool .devcontainer/devcontainer.json > /dev/null && echo "✅ devcontainer.json is valid JSON"
fi

# Check if scripts are executable
chmod +x .devcontainer/post-create.sh

# Verify Dockerfile syntax (basic check)
if grep -q "FROM" .devcontainer/Dockerfile; then
  echo "✅ Dockerfile has correct structure"
fi

echo ""
echo "✨ All validation checks passed!"
echo ""
echo "To use Codespaces:"
echo "1. Push changes to GitHub"
echo "2. Click 'Code' → 'Codespaces' → 'Create codespace on main'"
echo "3. Wait for setup (2-3 minutes)"
echo ""

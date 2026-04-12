# Developing with GitHub Codespaces

This guide explains how to set up and use GitHub Codespaces for ScanAPI development.

## 🚀 Quick Start

1. **Open the repository in Codespaces:**
   - Go to the ScanAPI repository on GitHub
   - Click `Code` → `Codespaces` → `Create codespace on main`
   - Wait for the environment to be configured (takes ~2-3 minutes on first run)

2. **After initialization:**
   - The setup script will run automatically (`.devcontainer/post-create.sh`)
   - All dependencies will be installed
   - Pre-commit hooks will be configured
   - You're ready to develop!

## 📋 Requirements

None! Codespaces provides everything you need:
- ✅ Python 3.12
- ✅ Git
- ✅ uv (fast package manager)
- ✅ VS Code with pre-configured extensions
- ✅ All project dependencies

## 🛠️ Environment Setup

### What gets installed automatically?

The `.devcontainer/devcontainer.json` configures:

**System Dependencies:**
- Git
- cURL
- Build essentials
- cryptography libraries

**Python Tools:**
- `uv` - Modern package manager (faster than pip)
- `pytest` - Testing framework
- `ruff` - Linter and formatter
- `mypy` - Type checker
- `sphinx` - Documentation
- `pre-commit` - Git hooks

**VS Code Extensions:**
- Python (Microsoft)
- Pylance - Advanced IntelliSense
- Debugger
- Black Formatter
- Ruff Linter
- MyPy Type Checker
- GitLens
- GitHub Copilot

## 📝 Common Commands

```bash
# Run tests with coverage
make test

# Check linting (ruff)
make lint

# Check types (mypy)
make mypy

# Run both (lint + mypy)
make check

# Format code
make format

# Test specific file
uv run pytest tests/unit/test_config_loader.py -v

# Run specific test
uv run pytest tests/unit/test_config_loader.py::test_name -v

# View coverage with HTML report
uv run pytest --cov=scanapi --cov-report=html
```

## 🧪 Testing with Examples

The `examples` repository is **automatically cloned during setup** at `/workspaces/examples`. You can test ScanAPI with real API specifications right away!

### Available Examples

**PokèAPI**

```bash
uv run scanapi run ../examples/pokeapi/scanapi.yaml -c ../examples/pokeapi/scanapi.conf -o ../examples/pokeapi/scanapi-report.html
# Open: ../examples/pokeapi/scanapi-report.html
```

**Demo-API**

```bash
uv run scanapi run ../examples/demo-api/scanapi.yaml -c ../examples/demo-api/scanapi.conf -o ../examples/demo-api/scanapi-report.html
# Open: ../examples/demo-api/scanapi-report.html
```

### Workspace Structure

After setup, your `/workspaces/` looks like:

```
/workspaces/
├── scanapi/           # Main project
├── examples/          # Test examples (auto-cloned)
```

Perfect for testing and learning!

## 🔧 Customization

### Modify the setup

Edit `.devcontainer/post-create.sh` to add:
- New Python dependencies: add to `pyproject.toml`
- System packages: add to `Dockerfile`
- VS Code extensions: add to `devcontainer.json`

### VS Code Settings

Settings are in `.devcontainer/devcontainer.json` under `customizations.vscode.settings`. Customize:
- Line length (rulers)
- Auto-formatting
- Linter integration
- pytest behavior

## 🐛 Debugging

### Use VS Code debugger

1. Create a breakpoint in code (click on editor margin)
2. Run: `uv run pytest --pdb tests/unit/test_config_loader.py`
3. Use debugger controls (F10 step over, F11 step into, etc.)

### View detailed logs

```bash
# Verbose test logs
uv run pytest -vv tests/

# Logs with print statements
uv run pytest -s tests/

# Debugging with pdb
uv run pytest --pdb tests/
```

## 📚 Documentation

View documentation locally:

```bash
cd documentation
uv run make html
# Open documentation/build/html/index.html in your browser
```

## 🔄 Recreate the Container

If something goes wrong or you want to clean everything:

1. In VS Code, click the remote button (bottom left corner)
2. Select "Rebuild Container"
3. Wait ~2-3 minutes

## 🌐 Port Forwarding

Codespaces automatically forwards:
- **Port 8000** - For test/application servers
- **Port 9000** - For HTML documentation

When you start a server, VS Code will notify you about port availability.

## 💡 Tips

- **Use aliases:** Add `alias t='uv run pytest'` to your shell
- **Auto pre-commit:** Pre-commit checks code before commits
- **Continuous type checking:** MyPy is integrated in VS Code
- **Format on save:** Ruff automatically formats when you save

## ❓ Troubleshooting

**Issue:** Dependencies not installed
```bash
# Force reinstall
uv pip install -e ".[dev]" --force-reinstall
```

**Issue:** Pre-commit not working
```bash
# Reinstall pre-commit hooks
uv run pre-commit install --install-hooks
```

**Issue:** Imports not working in type checker
```bash
# Reinstall with type stubs (types-*)
uv pip install types-PyYAML types-requests types-setuptools
```

**Issue:** Container slow or problematic
- Rebuild: Click remote button → "Rebuild Container"
- Clear cache: `rm -rf .pytest_cache __pycache__ .ruff_cache`

## 📖 Next Steps

- Read [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Explore [First-Pull-Request.md](../wiki/First-Pull-Request.md)
- Check [Writing-Tests.md](../wiki/Writing-Tests.md) for testing best practices

---

**Need help?** Open an issue in the repository or find us in Discord/Slack!

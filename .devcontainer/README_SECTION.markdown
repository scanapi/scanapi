<!--
INSTRUCTION: Copy the section below to README.md of ScanAPI (after the Installation section)
-->

## 🚀 Getting Started with Development

### Option 1: GitHub Codespaces (Recommended - Zero Setup) ⭐

The fastest way to get started without installing anything!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/scanapi/scanapi)

**Or manually:**
1. Go to the repository: https://github.com/scanapi/scanapi
2. Click `<> Code` → `Codespaces` → `Create codespace on main`
3. Wait 2-3 minutes (first time is slower)
4. ✨ Done! VS Code in browser with Python 3.12 + all tools

No need to install anything locally!

**Available commands:**
```bash
make test        # Run tests with coverage
make lint        # Check code
make check       # Lint + type checking
make format      # Format code
```

📖 **[Complete Codespaces Guide](wiki/Codespaces-QuickStart.md)**

### Option 2: Local Dev Container

If you prefer local development with a containerized environment:

1. Clone the repository:
```bash
git clone https://github.com/scanapi/scanapi.git
cd scanapi
```

2. Open in VS Code:
```bash
code .
```

3. When VS Code asks, choose: **"Reopen in Container"**
   (Or use `Cmd+Shift+P` / `Ctrl+Shift+P` → "Dev Containers: Reopen in Container")

4. Wait 2-3 minutes

Everything will be installed automatically!

### Option 3: Manual Setup

If you prefer to install locally without a container:

**Requirements:**
- Python 3.10 or higher
- pip or uv

**Installation:**
```bash
# Clone
git clone https://github.com/scanapi/scanapi.git
cd scanapi

# Virtual environment
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
# or
.venv\Scripts\activate             # Windows

# Dependencies
pip install -e ".[dev]"            # Or: uv pip install -e ".[dev]"

# Test
pytest
```

## 📝 Common Commands

```bash
# Tests
make test                          # With coverage
uv run pytest -v tests/            # Detailed
uv run pytest --cov                # Coverage report

# Quality
make lint                          # Ruff linter
make mypy                          # Type checking
make check                         # Lint + MyPy
make format                        # Format code

# Debugging
uv run pytest --pdb tests/         # Interactive debugger
```

## 📚 Developer Documentation

- **[Codespaces Quick Start](wiki/Codespaces-QuickStart.md)** (30 seconds)
- **[Complete Guide (5-10 min)](wiki/Codespaces.md)**
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Project guidelines
- **[Writing Tests](wiki/Writing-Tests.md)** - Best practices
- **[Run Locally](wiki/Run-ScanAPI-Locally.md)** - Detailed setup

## 💡 Tip

**GitHub Codespaces is the fastest way!** You can get started in seconds without installing anything. Perfect for:
- ✅ First contributions
- ✅ Quick fixes
- ✅ Testing before PR
- ✅ Demo for friends

---

<!-- END OF INSTRUCTION -->

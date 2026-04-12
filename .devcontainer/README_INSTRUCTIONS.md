## Instructions for Adding to ScanAPI README.md

Add the section below in the "Getting Started" or "Development" section of the main README:

---

### 🚀 Quick Start with GitHub Codespaces

To start developing **without installing anything**, use GitHub Codespaces:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/scanapi/scanapi)

**Or manually:**
1. Go to the repository on GitHub
2. Click `<> Code` → `Codespaces` → `Create codespace on main`
3. Wait 2-3 minutes
4. **Done!** All commands below work:

```bash
make test       # Tests with coverage
make lint       # Code check
make check      # Lint + Type checking
make format     # Format code
```

📖 [See complete Codespaces guide →](wiki/Codespaces-QuickStart.md)

---

### 🖥️ Local Setup with Dev Container

If you prefer to develop locally with a containerized environment:

1. Clone the repository: `git clone https://github.com/scanapi/scanapi.git`
2. Open in VS Code: `code scanapi`
3. Open command palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
4. Type: `Dev Containers: Reopen in Container`
5. Wait 2-3 minutes

All requirements (Python 3.12, dependencies, tools) will be installed automatically!

---

### ⚙️ Manual Setup

If you prefer to configure manually:

```bash
# Requirements
- Python 3.10+
- pip or uv

# Clone and access
git clone https://github.com/scanapi/scanapi.git
cd scanapi

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or: .venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Test the installation
pytest
```

---

**💡 Tip:** GitHub Codespaces is the fastest way! You can get started in seconds.

---

## Added Files Structure

```
.devcontainer/
  ├── devcontainer.json      # Main configuration
  ├── Dockerfile             # Container image
  ├── post-create.sh         # Auto setup
  ├── validate.sh            # Configuration validation
  └── README.md              # Technical documentation

wiki/
  ├── Codespaces-QuickStart.md  # Quick reference
  └── Codespaces.md             # Complete guide
```

## Badge for GitHub README

Copy and paste this in your README.md to add a visual badge:

```markdown
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/scanapi/scanapi)
```

Or simply:

```markdown
[💻 Open in Codespaces](https://codespaces.new/scanapi/scanapi)
```

---

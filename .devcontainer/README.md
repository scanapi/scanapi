# 🐳 GitHub Codespaces Configuration

This directory contains the GitHub Codespaces configuration for ScanAPI.

## Configuration Files

### `devcontainer.json`
Main Dev Container configuration file. Defines:
- **Base image:** Python 3.12 (Bullseye)
- **Features:** Git and GitHub CLI
- **VS Code Extensions:** Python, Pylance, Ruff, MyPy, GitLens, etc.
- **Editor settings:** Auto-formatting, ruff linting, pytest
- **Ports:** 8000 (server) and 9000 (documentation)
- **Post-creation script:** `post-create.sh`

### `post-create.sh`
Script automatically executed after the container is created:
- Updates system packages
- Installs `uv` (fast package manager)
- Installs project dependencies with `uv pip install -e ".[dev]"`
- Configures pre-commit hooks
- Runs initial verification checks

### `Dockerfile`
Defines the container image:
- Base: `python:1-3.12-bullseye`
- Installs additional tools: git, curl, build-essential, zsh
- Installs `uv` for package management
- Sets Python environment variables

### `validate.sh`
Script to validate the configuration:
```bash
bash .devcontainer/validate.sh
```

## 🚀 How to Use

### Open in Codespaces
```bash
# Via GitHub
1. Go to the repository
2. Code → Codespaces → Create codespace on main
3. Wait 2-3 minutes

# Via CLI (if gh is installed)
gh codespace create -b main -R scanapi/scanapi
```

### Open locally with Dev Container
```bash
# VS Code: Cmd+Shift+P
# Type: "Dev Containers: Reopen in Container"
```

## 📋 Dependencies Structure

```
Python 3.12
├── Runtime
│   ├── appdirs, curlify2, rich, PyYAML, Jinja2, click
│   ├── httpx, packaging, restrictedpython
│   └── MarkupSafe (pinned: 3.0.3)
└── Development
    ├── Testing: pytest, pytest-cov, pytest-freezegun, pytest-mock
    ├── Linting: ruff, pre-commit
    ├── Type checking: mypy, types-*
    ├── Documentation: sphinx, sphinx_rtd_theme
    └── Security: bandit, requests-mock
```

## 🔧 Customization

### Add VS Code Extensions
In `devcontainer.json`, modify the section:
```json
"extensions": [
  "publisher.extension-id",
  // ... add more
]
```

### Add Python Dependencies
In `pyproject.toml`:
```toml
dev = [
  # ... add here
  "new-dependency>=1.0"
]
```

### Modify Setup
Edit `post-create.sh` to add custom commands.

## 🌍 Environment Variables

If you need environment variables, add them in `devcontainer.json`:
```json
"remoteEnv": {
  "VARIABLE_NAME": "value"
}
```

## 📚 Resources

- [Dev Containers Documentation](https://containers.dev/)
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [ScanAPI Development Guide](../wiki/Codespaces.md)
- [Contributing Guide](../CONTRIBUTING.md)

## ✅ Verifying Configuration

```bash
# Inside the container, verify:
python --version        # Python 3.12
uv --version           # uv package manager
which ruff             # Should return path
which mypy             # Should return path
which pytest           # Should return path
```

## 🐛 Troubleshooting

**Issue:** Container won't start
- Recreate: Click remote button → "Rebuild Container"

**Issue:** Dependencies not found
- Reinstall: `uv pip install -e ".[dev]" --force-reinstall`

**Issue:** .devcontainer ignored in Codespaces
- Commit and push: Git add → commit → push
- Create new codespace (don't use old ones)

---

For complete documentation, see [Codespaces.md](../wiki/Codespaces.md)

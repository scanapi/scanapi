# GitHub Codespaces Quick Start

[Full Documentation →](Codespaces.md)

## 30 Seconds to Setup

1. Go to the repository → `Code` → `Codespaces`
2. Click `Create codespace on main`
3. Wait ~2-3 minutes
4. **Done!** All commands below work:

```bash
make test
make lint
make check
make format
```

## After Cloning Locally

If you cloned the repository and want to use Codespaces:

```bash
# In VS Code, open command palette (Cmd+Shift+P on Mac)
# Type: "Dev Containers: Reopen in Container"
```

## Using Codespaces? ✅

- ✨ Python 3.12 pre-installed
- 🚀 uv for fast package management
- 🧪 pytest pre-configured
- 📝 ruff + mypy + pre-commit integrated
- 💻 GitHub Copilot available
- 🔗 Ports 8000 and 9000 forwarded

## Main Commands

| Command | What it does |
|---------|-------------|
| `make test` | Run tests with coverage |
| `make lint` | Check code with ruff |
| `make mypy` | Type checking |
| `make check` | Lint + MyPy |
| `make format` | Auto-format code |

## 🧪 Test with Examples

Examples are auto-cloned during setup! Quick test:

```bash
# PokèAPI example
uv run scanapi run ../examples/pokeapi/scanapi.yaml -c ../examples/pokeapi/scanapi.conf -o ../examples/pokeapi/scanapi-report.html

# Demo-API example
uv run scanapi run ../examples/demo-api/scanapi.yaml -c ../examples/demo-api/scanapi.conf -o ../examples/demo-api/scanapi-report.html
```

---

👉 See [Codespaces.md](Codespaces.md) for full documentation!

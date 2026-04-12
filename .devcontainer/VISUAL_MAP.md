# 🎯 Visual Map - ScanAPI Codespaces Configuration

## Startup Flow

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub → Code → Codespaces → Create codespace on main      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  GitHub Codespaces     │
        │  Wait 2-3 minutes      │
        └────────────┬───────────┘
                     │
        ┌────────────▼───────────┐
        │ .devcontainer/         │
        │ runs again             │
        └────────────┬───────────┘
                     │
        ┌────────────▼──────────────────────────┐
        │ 1. Update packages (apt)              │
        │ 2. Install uv                         │
        │ 3. Install dependencies (.dev)        │
        │ 4. Clone examples repo                │
        │ 5. Setup pre-commit                   │
        │ 6. Run initial checks                 │
        └────────────┬──────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │ ✨ Ready for DEV!                   │
        │                                     │
        │ VS Code + Extensions                │
        │ Python 3.12                         │
        │ All tools                           │
        │ Examples repo cloned & ready        │
        └────────────────────────────────────┘
```

## File Structure - What You Got

```
scanapi/
├── .devcontainer/                    ← 🆕 ADDED
│   ├── devcontainer.json            # Main config (JSON)
│   ├── Dockerfile                   # Image def (Python 3.12)
│   ├── post-create.sh               # Setup script (executable)
│   ├── validate.sh                  # Validation (executable)
│   ├── README.md                    # Technical docs
│   ├── SETUP_COMPLETE.md            # Checklist
│   └── README_INSTRUCTIONS.md       # README instructions
│
├── wiki/                             ← 🆕 ADDED
│   ├── Codespaces-QuickStart.md     # 30s reference
│   └── Codespaces.md                # 5-10 min guide
│
├── pyproject.toml                   # (existing - not modified)
├── Makefile                         # (existing - not modified)
├── README.md                        # (we suggest adding badge)
└── ... (rest of project)
```

## Installed Dependencies

```
System (apt)
├── git
├── curl
├── build-essential
├── libssl-dev
└── zsh

Python 3.12
├── Runtime (from pyproject.toml)
│   ├── appdirs, curlify2, rich
│   ├── PyYAML, Jinja2, click
│   ├── httpx, packaging
│   └── restrictedpython
│
└── Development (optional)
    ├── Testing
    │   ├── pytest, pytest-cov
    │   ├── pytest-freezegun
    │   └── pytest-mock
    ├── Linting
    │   ├── ruff, pre-commit
    │   └── bandit
    ├── Type Checking
    │   ├── mypy
    │   └── types-* (PyYAML, requests, setuptools)
    └── Docs
        ├── sphinx
        └── sphinx_rtd_theme

Tools
├── uv (package manager)
└── pre-commit (git hooks)
```

## Dev Container Architecture

```
┌─────────────────────────────────────────┐
│  GitHub Codespaces / Dev Container      │
├─────────────────────────────────────────┤
│                                          │
│  VS Code Browser Interface               │
│  ├── Python Extension                    │
│  ├── Pylance (IntelliSense)              │
│  ├── Ruff Linter (real-time)             │
│  ├── MyPy Type Checker (real-time)       │
│  ├── Debugger (F5)                       │
│  ├── Integrated Terminal                 │
│  └── Pre-commit Integration              │
│                                          │
├─────────────────────────────────────────┤
│  Container (Linux/Bullseye)              │
│  ├── Python 3.12                         │
│  ├── uv (package manager)                │
│  ├── pytest (testing framework)          │
│  ├── ruff (linter/formatter)             │
│  ├── mypy (type checker)                 │
│  ├── sphinx (documentation)              │
│  ├── pre-commit (git hooks)              │
│  └── Git + GitHub CLI                    │
│                                          │
├─────────────────────────────────────────┤
│  Forwarded Ports                         │
│  ├── 8000 (app server)                   │
│  └── 9000 (documentation)                │
└─────────────────────────────────────────┘
```

## Available Commands

```bash
# Anywhere (using make)
make test           # pytest with coverage
make lint           # ruff check
make mypy           # type checking
make check          # lint + mypy
make format         # ruff fix + format

# Direct with uv
uv run pytest tests/
uv run ruff check .
uv run mypy scanapi

# Manual pre-commit
uv run pre-commit run --all-files
```

## Development Workflow

```
┌─────────────────┐
│  Write code     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ VS Code detects:             │
│ - Syntax errors              │
│ - Type issues (MyPy)         │
│ - Linting problems (Ruff)    │
└────────┬────────────────────┘
         │
         ├─ Auto fix (on save)
         │
         ▼
┌──────────────────────────┐
│ git add / git commit     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Pre-commit hooks run     │
│ (verify code before)     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Push to repository       │
└──────────────────────────┘
```

## Support for Any Work Type

```
┌─────────────────────────────────────────────┐
│ Develop a Feature                           │
│ ├─ make check (lint + type checking OK?)    │
│ ├─ make test (all tests pass?)              │
│ └─ create PR (review and merge)             │
├─────────────────────────────────────────────┤
│ Write Tests                                 │
│ ├─ uv run pytest -v tests/                  │
│ ├─ uv run pytest --cov                      │
│ └─ uv run pytest -s (with prints)           │
├─────────────────────────────────────────────┤
│ Debugging                                   │
│ ├─ F5 (VS Code debugger)                    │
│ ├─ uv run pytest --pdb                      │
│ └─ breakpoints in code                      │
├─────────────────────────────────────────────┤
│ Documentation                               │
│ ├─ cd documentation                         │
│ ├─ uv run make html                         │
│ └─ Open build/html/index.html               │
└─────────────────────────────────────────────┘
```

## Setup Options Comparison

| Aspect | Codespaces | Dev Container Local | Manual Setup |
|--------|-----------|----------------------|--------------|
| **Setup** | 0 (in browser) | 0 (Git + VS Code) | Manual |
| **Time** | 2-3 min | 2-3 min | 5-10 min |
| **Hardware** | Cloud | Your PC | Your PC |
| **Internet** | Always | Clone only | For download |
| **Persistence** | Temp with backup | Local | Local |
| **Best for** | Quick starts | Local dev | Preference |

---

**End Result:**
✅ One click and you have **Python 3.12 + all tools** ready!

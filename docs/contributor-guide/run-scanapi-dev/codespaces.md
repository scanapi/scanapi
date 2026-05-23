# Run ScanAPI on GitHub Codespaces

> For the centralized comparison of all supported ScanAPI development environments, see [Run ScanAPI in Dev Env](index.md).

GitHub Codespaces gives you a ready-to-use development environment in the browser,
with everything preconfigured. With ScanAPI, that means you can start running tests
and generating reports in just a few minutes, without installing anything locally.

At this point, it is expected that you already:

* have a GitHub account
* forked the repository

## Table of Contents (TOC)
- [1. Open your fork in Codespaces](#1-open-your-fork-in-codespaces)
- [2. Wait for setup to finish](#2-wait-for-setup-to-finish)
- [3. Add the examples folder](#3-add-the-examples-folder)
  - [3.1 Add the folder](#31-add-the-folder)
  - [3.2 Save the workspace](#32-save-the-workspace)
  - [3.3 Reopen later](#33-reopen-later)
- [4. Verify the environment](#4-verify-the-environment)
  - [4.1 Check ScanAPI is installed](#41-check-scanapi-is-installed)
  - [4.2 Run project checks](#42-run-project-checks)
- [5. Run your first scan](#5-run-your-first-scan)
- [6. View the report (browser)](#6-view-the-report-browser)
- [7. Try another example](#7-try-another-example)
- [8. Troubleshooting](#8-troubleshooting)
  - [8.1 Rebuild container](#81-rebuild-container)
  - [8.2 Reinstall dependencies](#82-reinstall-dependencies)
  - [8.3 Fix pre-commit](#83-fix-pre-commit)
  - [8.4 Clear caches](#84-clear-caches)

## 1. Open your fork in Codespaces

- Go to your fork (e.g. `https://github.com/<your-user>/scanapi`)
- Click `Code` → `Codespaces` → `Create codespace on main`
- Wait about 2–3 minutes

When the Codespace opens, the setup runs automatically.

## 2. Wait for setup to finish

During initialization, the environment is fully prepared for you:

- dependencies are installed
- Python environment is configured
- development tools are set up

You’re ready when:

- the terminal stops running commands
- the README opens automatically

## 3. Add the examples folder

ScanAPI provides ready-to-run examples that we will use here to test and explore
the tool: https://github.com/scanapi/examples. This repository is already cloned
into:

```
/workspaces/examples
```

But it is not automatically added to VS Code, so you need to add it manually.

### 3.1 Add the folder

- Open Command Palette (`⌘⇧P` or `Ctrl+Shift+P`)
- Run: `Workspaces: Add Folder to Workspace...`
- Select: `/workspaces/examples`

You should now see:

- `scanapi/`
- `examples/`

### 3.2 Save the workspace

Saving avoids having to repeat this setup every time.

- Go to: `File → Save Workspace As...`
- Save as: `scanapi.code-workspace`
- Location: `/workspaces/`

This creates a workspace file that remembers both folders.

### 3.3 Reopen later

Next time you open the Codespace, you can restore everything with:

```bash
code /workspaces/scanapi.code-workspace
```

This reloads both `scanapi` and `examples` automatically.

## 4. Verify the environment

Before running your first scan, quickly check that everything is working.

### 4.1 Check ScanAPI is installed

```bash
uv run scanapi --version
```

You should see the installed version printed in the terminal.

### 4.2 Run project checks

```bash
make install   # ensures all of the dependencies are installed
make test      # runs tests to verify everything works
make lint      # checks code style with ruff
make mypy      # runs type checking
make check     # runs lint + mypy together
```

If these commands run without errors, your environment is correctly set up.

## 5. Run your first scan

Now that your environment is ready, it is time for you to run your first scan.

ScanAPI requires an API specification file to run. Instead of writing tests in
code, you define your API behavior in a YAML file. ScanAPI reads this file,
executes the defined requests, and validates the responses.

If you try to run ScanAPI without a specification file:

```bash
uv run scanapi
```

You will see an error like:

```bash
ERROR:scanapi:Could not find API spec file: scanapi.yaml.
```

This happens because ScanAPI looks for a `scanapi.yaml` file by default, which
was not found.

To get started quickly, let's use the examples repository. You can run your
first scan with:

```bash
uv run scanapi run ../examples/pokeapi/scanapi.yaml \
  -c ../examples/pokeapi/scanapi.conf \
  -o ../examples/pokeapi/scanapi-report.html
```

This will:

* execute API tests defined in the example
* generate an HTML report with the results

## 6. View the report (browser)

Open a second terminal and run:

```bash
cd /workspaces && python -m http.server 8000
```

Then:

* Click “Open in Browser” in the popup

You’ll see a file browser with:

* `scanapi/`
* `examples/`

Open your report at:

```
examples/pokeapi/scanapi-report.html
```

You can use this view to navigate and open any generated HTML report.

## 7. Try another example

Once you've successfully run your first scan, you can explore other examples to
better understand how ScanAPI works with different APIs and configurations.

The repository includes multiple ready-to-run scenarios.

Some of the scenarios have their own environment setup. To turn on this environment run.

```bash
source ../examples/demo-api/.env
```

Afterwards you can run the scenario.

```bash
uv run scanapi run ../examples/demo-api/scanapi.yaml \
  -c ../examples/demo-api/scanapi.conf \
  -o ../examples/demo-api/scanapi-report.html
```

## 8. Troubleshooting

If something doesn’t work as expected, the steps below cover the most common issues
and how to fix them. Use these commands to reset or repair your environment when needed.

### 8.1 Rebuild container

If something is broken or outdated:

* Open Command Palette
* Run: `Rebuild Container`

This recreates the environment from scratch.

### 8.2 Reinstall dependencies

If something seems inconsistent or broken:

```bash
uv pip install -e ".[dev]" --force-reinstall
```

This reinstalls all project dependencies.

### 8.3 Fix pre-commit

If hooks are not running:

```bash
uv run pre-commit install --install-hooks
```

This ensures checks run automatically before commits.

### 8.4 Clear caches

If you see strange test or lint behavior:

```bash
rm -rf .pytest_cache __pycache__ .ruff_cache
```

This removes cached files that might cause inconsistencies.

# Run ScanAPI locally with Dev Container

> For the centralized comparison of all supported ScanAPI development environments, see [Run ScanAPI in Dev Env](Run-ScanAPI-in-Dev-Env.md).

Running ScanAPI using a Dev Container is an alternative to manual setup.

It allows you to:

* use a pre-configured environment with all dependencies installed
* avoid conflicts with your local system
* work in the same setup used in Codespaces and CI

This guide walks you through how to open the project in a Dev Container,
verify the setup, run your first scan, and view the results.

At this point, it is expected that you already:

* have a GitHub account
* forked the repository

## Dev Container setup

## 1. Install requirements

Make sure you have the following installed:

- VS Code: https://code.visualstudio.com/
- Dev Containers extension: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
- Docker: https://docs.docker.com/get-docker/

## 2. Clone your fork

Clone your fork locally and enter the project folder:

```bash
git clone git@github.com:your-username/scanapi.git
cd scanapi
```

Replace `your-username` with your GitHub username.

## 3. Open in Dev Container

Open the project in VS Code.

Then:

* Click **"Reopen in Container"** when prompted
  or
* Open Command Palette (`⌘⇧P` or `Ctrl+Shift+P`) and run:
  `Dev Containers: Reopen in Container`

Wait for the container to build (first time takes ~2–3 minutes).

## 4. Verify the environment

The Dev Container automatically:

* installs all dependencies
* configures the Python environment
* sets up pre-commit hooks
* clones the examples repository

Before running your first scan, check that everything is working correctly.

### 4.1 Check ScanAPI version

```bash
uv run scanapi --version
```

### 4.2 Run project checks

```bash
make test      # run tests
make lint      # check code style
make mypy      # type checking
make check     # lint + mypy
```

If these commands run without errors, your environment is correctly set up.

## 5. Run your first scan

Now that your environment is ready, it is time to run your first scan.

ScanAPI requires an API specification file to run. Instead of writing tests in
code, you define your API behavior in a YAML file. ScanAPI reads this file,
executes the requests, and validates the responses.

If you try to run ScanAPI without a specification file:

```bash
uv run scanapi
```

You will see an error like:

```bash
ERROR:scanapi:Could not find API spec file: scanapi.yaml.
```

This happens because ScanAPI looks for a `scanapi.yaml` file by default.

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

## 6. View the report

After running a scan, ScanAPI generates an HTML report with the results.

Open the generated file:

```
../examples/pokeapi/scanapi-report.html
```

## 7. Try another example

Once you've successfully run your first scan, you can explore other examples to
better understand how ScanAPI works with different APIs and configurations.

```bash
uv run scanapi run ../examples/demo-api/scanapi.yaml \
  -c ../examples/demo-api/scanapi.conf \
  -o ../examples/demo-api/scanapi-report.html
```

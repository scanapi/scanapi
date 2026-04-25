# Run ScanAPI locally manually

> For the centralized comparison of all supported ScanAPI development environments, see [Run ScanAPI in Dev Env](Run-ScanAPI-in-Dev-Env.md).

Running ScanAPI locally is an important step when contributing to the project.
It allows you to:

* confirm your environment is correctly set up
* run tests before and after your changes
* validate that your changes behave as expected
* experiment with real API scenarios using examples

This guide walks you through how to set up ScanAPI locally, run your first scan,
and view the generated reports.

At this point, it is expected that you already:

* have a GitHub account
* forked the repository

## Local Setup

## 1. Install requirements

Make sure you have the following installed:

- Python 3.10+
- uv (https://docs.astral.sh/uv/#installation)

## 2. Clone your fork

Clone your fork locally and enter the project folder:

```bash
git clone git@github.com:your-username/scanapi.git
cd scanapi
```

Replace `your-username` with your GitHub username.

## 3. Clone the examples repository

ScanAPI provides ready-to-run examples that we will use here to test and explore
the tool:
[https://github.com/scanapi/examples](https://github.com/scanapi/examples)

Open another terminal (outside the `scanapi` folder) and clone:

```bash
git clone git@github.com:scanapi/examples.git
```

Your workspace should now look like:

```
scanapi/
examples/
```

## 4. Install dependencies

Install all project dependencies (inside scanapi folder):

```bash
make install
```

## 5. Verify the environment

Before running your first scan, check that everything is working correctly.

### 5.1 Check ScanAPI version

```bash
uv run scanapi --version
```

### 5.2 Run project checks

```bash
make test      # run tests
make lint      # check code style
make mypy      # type checking
make check     # lint + mypy
```

If these commands run without errors, your environment is correctly set up.

## 6. Run your first scan

Now that your environment is ready, it is time to run your first scan.

ScanAPI requires an API specification file to run. Instead of writing tests in
code, you define your API behavior in a YAML file. ScanAPI reads this file,
executes the requests, and validates the responses.

If you try to run ScanAPI without a specification file:

```bash
uv run scanapi run
```

You will see an error like:

```plaintext
ERROR    Could not find API spec file: scanapi.yaml. [Errno 2] No such file or directory: 'scanapi.yaml'
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

## 7. View the report

After running a scan, ScanAPI generates an HTML report with the results.

Open the generated file:

```
../examples/pokeapi/scanapi-report.html
```

## 8. Try another example

Once you've successfully run your first scan, you can explore other examples to
better understand how ScanAPI works with different APIs and configurations.

```bash
uv run scanapi run ../examples/demo-api/scanapi.yaml \
  -c ../examples/demo-api/scanapi.conf \
  -o ../examples/demo-api/scanapi-report.html
```

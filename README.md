![](https://github.com/scanapi/design/raw/master/images/github-hero-dark.png)

<p align="center">
  <a href="https://app.circleci.com/pipelines/github/scanapi/scanapi?branch=master">
    <img alt="CircleCI" src="https://img.shields.io/circleci/build/github/scanapi/scanapi">
  </a>
  <a href="https://codecov.io/gh/scanapi/scanapi">
    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/scanapi/scanapi">
  </a>
  <a href="https://badge.fury.io/py/scanapi">
    <img alt="PyPI version" src="https://badge.fury.io/py/scanapi.svg">
  </a>
</p>

A library for **your API** that provides:

- Automated Integration Testing
- Automated Live Documentation

Given an API specification, written in YAML/JSON format, ScanAPI hits the specified
endpoints, runs the test cases, and generates a detailed report of this execution - that can be
also used as the API documentation itself.

With almost none Python knowledge, the user can define endpoints to be hit, the expected behaviors
for each response, and, as a result, receives a full real-time diagnostic of the API!

## Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [How to install](#how-to-install)
- [Basic Usage](#basic-usage)
- [Documentation](#documentation)
  - [ScanAPI CLI](#scanapi-cli)
  - [API Specification Keys](#api-specification-keys)
  - [Environment Variables](#environment-variables)
  - [Custom Variables](#custom-variables)
  - [Python Code](#python-code)
  - [Chaining Requests](#chaining-requests)
  - [API specification in multiple files](#api-specification-in-multiple-files)
  - [Configuration File](#configuration-file)
  - [Hiding sensitive information](#hiding-sensitive-information)
- [Contributing](#contributing)

## Requirements

- [pip][pip-installation]

## How to install

```bash
$ pip install scanapi
```

## Basic Usage

You will need to write the API's specification and save it as an **YAML** or **JSON** file.
For example:

```yaml
api:
  endpoints:
    - name: scanapi-demo # The API's name of your API
      path: http://demo.scanapi.dev/api/ # The API's base url
      requests:
        - name: list_all_devs # The name of the fist request
          path: devs/ # The path of the fist request
          method: get # The HTTP method of the fist request
          tests:
            - name: status_code_is_200 # The name of the first test for this request
              assert: ${{ response.status_code == 200 }} # The assertion
```

And run the scanapi command

```bash
$ scanapi <file_path>
```

Then, the lib will hit the specified endpoints and generate a `scanapi-report.html` file with the
report results.

<p align="center">
  <img
    src="https://github.com/scanapi/scanapi/blob/master/images/report-print-closed.png"
    width="700",
    alt="An overview screenshot of the report."
  >
  <img
    src="https://github.com/scanapi/scanapi/blob/master/images/report-print-request.png"
    width="700"
    alt="A screenshot of the report showing the request details."
  >
  <img
    src="https://github.com/scanapi/scanapi/blob/master/images/report-print-response.png"
    width="700",
    alt="A screenshot of the report showing the response and test details"
  >
</p>

You can find complete examples at [scanapi/examples][scanapi-examples]!

## Documentation

### ScanAPI CLI

```
$ scanapi --help
Usage: scanapi [OPTIONS] [SPEC_PATH]

  Automated Testing and Documentation for your REST API. SPEC_PATH argument
  is the API specification file path.

Options:
  -o, --output-path PATH          Report output path.
  -c, --config-path PATH          Configuration file path.
  -t, --template PATH             Custom report template path.
  -ll, --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set the debug logging level for the program.
  -h, --help                      Show this message and exit.
```

### Syntax - API Specification Keys

| KEY              | Description                                                                                         | Type   | Scopes                            |
| ---------------- | --------------------------------------------------------------------------------------------------- | ------ | --------------------------------- |
| api              | It is reserver word that marks the root of the specification and must not appear in any other place | dict   | root                              |
| assert           | The test assertion                                                                                  | dict   | tests                             |
| body             | The HTTP body of the request                                                                        | dict   | request                           |
| endpoints        | It represents a list of API endpoints                                                               | list   | endpoint                          |
| headers          | The HTTP headers                                                                                    | dict   | endpoint, request                 |
| method           | The HTTP method of the request (GET, POST, PUT, PATCH or DELETE). If not set, GET will be used      | string | request                           |
| name             | An identifier                                                                                       | string | endpoint, request, test           |
| params           | The HTTP query parameters                                                                           | dict   | endpoint, request                 |
| path             | A part of the URL path that will be concatenated with possible other paths                          | string | endpoint, request                 |
| requests         | It represents a list of HTTP requests                                                               | list   | endpoint                          |
| tests            | It represents a list of tests to run against a HTTP response of a request                           | list   | request                           |
| vars             | Key used to define your custom variables to be used along the specification                         | dict   | endpoint, request                 |
| ${custom var}    | A syntax to get the value of the custom variables defined at key `vars`                             | string | request - after `vars` definition |
| ${ENV_VAR}       | A syntax to get the value of an environment variable                                                | string | endpoint, request                 |
| ${{python_code}} | A syntax to get the value of a Python code expression                                               | string | request                           |


### Environment Variables

You can use environment variables in your API spec file with the syntax

```yaml
${MY_ENV_VAR}
```

For example:

```bash
$ export BASE_URL="http://demo.scanapi.dev/api/"
```

```yaml
api:
  endpoints:
    - name: scanapi-demo
      path: ${BASE_URL}
      requests:
        - name: health
          method: get
          path: /health/
```

ScanAPI would call the following `http://demo.scanapi.dev/api/health/` then.

**Heads up: the variable name must be in upper case.**

### Custom Variables

You can create custom variables using the syntax:

```yaml
requests:
  - name: my_request
    ...
    vars:
      my_variable_name: my_variable_value
```

And in the next requests you can access them using the syntax:


```yaml
${my_variable_name}
```

### Python Code

You can add Python code to the API specification by using the syntax:

```yaml
${{my_pyhon_code}}
```

For example

```yaml
body:
  uuid: 5c5af4f2-2265-4e6c-94b4-d681c1648c38
  name: Tarik
  yearsOfExperience: ${{2 + 5}}
  languages:
    - ruby
      go
  newOpportunities: false
```

What I can use inside the `${{}}` syntax?
Basically any python code that **can run inside an `eval` python command**.
A short list of modules will be already available for you. They are all the imports of
[this file](https://github.com/scanapi/scanapi/blob/master/scanapi/evaluators/code_evaluator.py#L1).

### Chaining Requests

Inside the request scope, you can save the results of the resulted response to use in the next
requests. For example:

```yaml
requests:
  - name: list_all
    method: get
    vars:
      dev_id: ${{response.json()[2]["uuid"]}}
```

The dev_id variable will receive the `uuid` value of the 3rd result from the devs_list_all request

It the response is

```json
[
    {
        "uuid": "68af402f-1084-40a4-b9b2-6bb5c2d11559",
        "name": "Anna",
        "yearsOfExperience": 5,
        "languages": [
            "python",
            "c"
        ],
        "newOpportunities": true
    },
    {
        "uuid": "0d1bd106-c585-4d6b-b3a4-d72dedf7190e",
        "name": "Louis",
        "yearsOfExperience": 3,
        "languages": [
            "java"
        ],
        "newOpportunities": true
    },
    {
        "uuid": "129e8cb2-d19c-41ad-9921-cea329bed7f0",
        "name": "Marcus",
        "yearsOfExperience": 4,
        "languages": [
            "c"
        ],
        "newOpportunities": false
    }
]
```

The dev_id variable will receive the value `129e8cb2-d19c-41ad-9921-cea329bed7f0`

### API specification in multiple files

With `!include`, it is possible to build your API specification in multiple files.

For example, these two files

```yaml
# api.yaml
api:
  endpoints:
    - name: scanapi-demo
      path: ${BASE_URL}
      requests: !include include.yaml
```

```yaml
# include.yaml
- name: health
  path: /health/
```

would generate:

```yaml
api:
  endpoints:
    - name: scanapi-demo
      path: ${BASE_URL}
      requests:
        - name: health
          path: /health/
```

### Configuration File

If you want to configure the ScanAPI with a file, you can create a `.scanapi.yaml` file in the root
of your project

```yaml
project_name: DemoAPI # This will be rendered in the Report Title.
spec_path: my_path/api.yaml # API specification file path
output_path: my_path/my-report.html # Report output path.
template: my_template.jinja # Custom report template path.
```

### Hiding sensitive information

If you want to omit sensitive information in the report, you can configure it in the `.scanapi.yaml`
file.

```yaml
report:
  hide-request:
    headers:
      - Authorization
```

The following configuration will print all the headers values for the `Authorization` key for all
the request as `SENSITIVE_INFORMATION` in the report.

In the same way you can omit sensitive information from response.

```yaml
report:
  hide-response:
    headers:
      - Authorization
```

Available attributes to hide: `headers`, `body` and `url`.

## Contributing

Collaboration is super welcome! We prepared the [CONTRIBUTING.md][contributing-file] file to help
you in the first steps. Every little bit of help counts! Feel free to create new GitHub issues and
interact here.

Let's built it together 🚀

[contributing-file]: https://github.com/scanapi/scanapi/blob/master/CONTRIBUTING.md
[pip-installation]: https://pip.pypa.io/en/stable/installing/
[scanapi-examples]: https://github.com/scanapi/examples

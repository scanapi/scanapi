<img src="https://user-images.githubusercontent.com/2728804/73694724-6d019080-46b7-11ea-8960-70db8f9b0a29.png"/>

[![CircleCI](https://circleci.com/gh/scanapi/scanapi.svg?style=svg)](https://circleci.com/gh/scanapi/scanapi)
[![codecov](https://codecov.io/gh/scanapi/scanapi/branch/master/graph/badge.svg)](https://codecov.io/gh/scanapi/scanapi)
[![PyPI version](https://badge.fury.io/py/scanapi.svg)](https://badge.fury.io/py/scanapi)
[![Gitter chat](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/scanapi/community)

A library for **your API** that provides:

- Automated Integration Testing
- Automated Live Documentation

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

```yaml
api:
  endpoints:
    - name: scanapi-demo
      path: http://demo.scanapi.dev/api/
      requests:
        - name: list_all_devs
          path: devs/
          method: get
```

And run the scanapi command

```bash
$ scanapi -s <file_path>
```

Then, the lib will hit the specified endpoints and generate a `scanapi-report.md` file with the report results

<p align="center">
  <img src="https://user-images.githubusercontent.com/2728804/80041097-ed26dd80-84d1-11ea-9c12-16d4a2a15183.png" width="700">
  <img src="https://user-images.githubusercontent.com/2728804/80041110-f7e17280-84d1-11ea-8290-2c09eefe6134.png" width="700">
</p>

You can find a complete example of a demo project using ScanAPI at [scanapi-demo][scanapi-demo]!

## Documentation

### ScanAPI CLI

```bash
$ scanapi --help
Usage: scanapi [OPTIONS]

  Automated Testing and Documentation for your REST API.

Options:
  -s, --spec-path PATH
  -o, --output-path PATH
  -c, --config-path PATH
  -r, --reporter [console|markdown|html]
  -t, --template PATH
  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
  --help                          Show this message and exit.
```

### API Specification Keys

| KEY              | Description                                                                                         | Type   | Scopes                            |
| ---------------- | --------------------------------------------------------------------------------------------------- | ------ | --------------------------------- |
| api              | It is reserver word that marks the root of the specification and must not appear in any other place | dict   | root                              |
| body             | The HTTP body of the request                                                                        | dict   | request                           |
| endpoints        | It represents a list of API endpoints                                                               | list   | endpoint                          |
| headers          | The HTTP headers                                                                                    | dict   | endpoint, request                 |
| method           | The HTTP method of the request (GET, POST, PUT, PATCH or DELETE). If not set, GET will be used      | string | request                           |
| name             | An identifier                                                                                       | string | endpoint, request                 |
| path             | A part of the URL path that will be concatenated with possible other paths                          | string | endpoint, request                 |
| requests         | It represents a list of HTTP requests                                                               | list   | endpoint                          |
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

### Chaining Requests

Inside the request scope, you can save the results of the resulted response to use in the next requests

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

If you want to configure the ScanAPI with a file, you can create a `.scanapi.yaml` file in the root of your project

```yaml
spec_path: my_path/api.yaml
output_path: my_path/scanapi-report.md
reporter: console
```

### Hiding sensitive information

If you want to omit sensitive information in the report, you can configure it in the `.scanapi.yaml` file.

```yaml
report:
  hide-request:
    headers:
      - Authorization
```

The following configuration will print all the headers values for the `Authorization` key for all the request as `<sensitive_information>` in the report.

In the same way you can omit sensitive information from response.

```yaml
report:
  hide-response:
    headers:
      - Authorization
```

## Contributing

Collaboration is super welcome! We prepared the [CONTRIBUTING.md][contributing-file] file to help you in the first steps. Feel free to create new GitHub issues and interact here :)

[pip-installation]: https://pip.pypa.io/en/stable/installing/
[scanapi-demo]: https://github.com/camilamaia/scanapi-demo
[contributing-file]: https://github.com/camilamaia/scanapi/blob/master/CONTRIBUTING.md

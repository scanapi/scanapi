![](https://github.com/scanapi/design/raw/main/images/github-hero-dark.png)

<p align="center">
  <a href="https://codecov.io/gh/scanapi/scanapi">
    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/scanapi/scanapi">
  </a>
  <a href="https://github.com/scanapi/scanapi/actions/workflows/lint.yml?query=branch%3Amain">
    <img alt="LintCheck" src="https://github.com/scanapi/scanapi/workflows/Lint%20check/badge.svg?event=push">
  </a>
  <a href="https://github.com/scanapi/scanapi/actions/workflows/run-examples.yml?query=branch%3Amain">
    <img alt="Examples" src="https://github.com/scanapi/scanapi/actions/workflows/run-examples.yml/badge.svg?branch=main">
  </a>
  <a href="https://pypistats.org/packages/scanapi">
    <img alt="Downloads Per Month" src="https://shields.io/pypi/dm/scanapi">
  </a>
  <a href="https://pypi.org/project/scanapi/">
    <img alt="PyPI version" src="https://shields.io/pypi/v/scanapi">
  </a>
  <a href="https://discord.scanapi.dev">
    <img alt="Discord" src="https://img.shields.io/discord/847208162993242162?color=7389D8&label=discord&logo=6A7EC2&logoColor=ffffff&style=flat-square">
  </a>
</p>

A library for **your API** that provides:

- Automated Integration Testing
- Automated Live Documentation

Given an API specification, written in YAML/JSON format, ScanAPI hits the specified
endpoints, runs the test cases, and generates a detailed report of this execution - which can also
be used as the API documentation itself.

With almost no Python knowledge, the user can define endpoints to be hit, the expected behavior
for each response and will receive a full real-time diagnostic report of the API!

## Contents

- [Quick Start](#quick-start)
  - [Requirements](#requirements)
  - [How to install](#how-to-install)
  - [Basic Usage](#basic-usage)
- [Documentation](#documentation)
- [Tutorial](#tutorial)
- [Examples](#examples)
- [Contributing](#contributing)
- [Contributors](#️-contributors)
- [Supporters Through Time](#supporters-through-time)

## Quick Start

### Requirements

- [pip][pip-installation]

### How to install

```bash
$ pip install scanapi
```

### Basic Usage

You will need to write the API's specification and save it as a **YAML** or **JSON** file.
For example:

```yaml
endpoints:
  - name: scanapi-demo # The API's name of your API
    path: http://demo.scanapi.dev/api/v1 # The API's base url
    requests:
      - name: list_all_users # The name of the first request
        path: users/ # The path of the first request
        method: get # The HTTP method of the first request
        tests:
          - name: status_code_is_200 # The name of the first test for this request
            assert: ${{ response.status_code == 200 }} # The assertion
```

And run the scanapi command

```bash
$ scanapi run <file_path>
```

Then, the lib will hit the specified endpoints and generate a `scanapi-report.html` file with the report results.

<p align="center">
  <img
    src="https://raw.githubusercontent.com/scanapi/scanapi/main/images/report-print-closed.png"
    width="700",
    alt="An overview screenshot of the report."
  >
  <img
    src="https://raw.githubusercontent.com/scanapi/scanapi/main/images/report-print-opened.png"
    width="700"
    alt="A screenshot of the report showing the request details."
  >
</p>

## Documentation

The full documentation is available at [scanapi.dev][website]

## Tutorial

Get started with ScanAPI by following our [step-by-step tutorial][tutorial].

## Examples

You can find complete examples at [scanapi/examples][scanapi-examples]!

This tutorial helps you to create integration tests for your REST API using ScanAPI

[![Watch the video](https://raw.githubusercontent.com/scanapi/scanapi/main/images/youtube-scanapi-tutorial.png)](https://www.youtube.com/watch?v=JIo4sA8LHco&t=2s)

## Contributing

Collaboration is super welcome! We prepared the [Newcomers Guide][newcomers-guide] to help you in the first steps. Every little bit of help counts! Feel free to create new [GitHub issues][github-issues] and interact here.

Let's build it together 🚀🚀

## ❤️ Contributors

[![contributors](https://contrib.rocks/image?repo=scanapi/scanapi)](https://github.com/scanapi/scanapi/graphs/contributors)

_Made with [contrib.rocks](https://contrib.rocks)._

## Supporters Through Time

<div style="display: flex; gap: 20px; align-items: center;">
  <a href="https://www.lambdatest.com/?utm_source=scanapi&utm_medium=sponsor" target="_blank">
      <img src="https://www.lambdatest.com/blue-logo.png" style="vertical-align: middle;" width="100" />
  </a>
  <img src="./images/red-hat-logo.png" width="100" alt="Red Hat Logo">
</div>

[github-issues]: https://github.com/scanapi/scanapi/issues
[newcomers-guide]: wiki/Newcomers.md
[pip-installation]: https://pip.pypa.io/en/stable/installing/
[scanapi-examples]: https://github.com/scanapi/examples
[tutorial]: https://scanapi.dev/tutorials/step01
[website]: https://scanapi.dev

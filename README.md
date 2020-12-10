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
  <a href="https://spectrum.chat/scanapi">
    <img alt="Join the community on Spectrum" src="https://withspectrum.github.io/badge/badge.svg" />
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

- [Contents](#contents)
- [Requirements](#requirements)
- [How to install](#how-to-install)
- [Basic Usage](#basic-usage)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributing](#contributing)

## Requirements

- [pip][pip-installation]

## How to install

```bash
$ pip install scanapi
```

## Basic Usage

You will need to write the API's specification and save it as a **YAML** or **JSON** file.
For example:

```yaml
endpoints:
  - name: scanapi-demo # The API's name of your API
    path: http://demo.scanapi.dev/api/ # The API's base url
    requests:
      - name: list_all_devs # The name of the first request
        path: devs/ # The path of the first request
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
    src="https://raw.githubusercontent.com/scanapi/scanapi/master/images/report-print-closed.png"
    width="700",
    alt="An overview screenshot of the report."
  >
  <img
    src="https://raw.githubusercontent.com/scanapi/scanapi/master/images/report-print-request.png"
    width="700"
    alt="A screenshot of the report showing the request details."
  >
  <img
    src="https://raw.githubusercontent.com/scanapi/scanapi/master/images/report-print-response.png"
    width="700",
    alt="A screenshot of the report showing the response and test details"
  >
</p>

## Documentation
The full documentation is available at [scanapi.dev][website]

## Examples
You can find complete examples at [scanapi/examples][scanapi-examples]!

This tutorial helps you to create integration tests for your REST API using ScanAPI

[![Watch the video](https://raw.githubusercontent.com/scanapi/scanapi/master/images/youtube-scanapi-tutorial.png)](https://www.youtube.com/watch?v=JIo4sA8LHco&t=2s)

## Contributing

Collaboration is super welcome! We prepared the [Newcomers Guide][newcomers-guide] to help you in the first steps. Every little bit of help counts! Feel free to create new [GitHub issues][github-issues] and interact here.

Let's build it together 🚀

[github-issues]: https://github.com/scanapi/scanapi/issues
[newcomers-guide]: https://github.com/scanapi/scanapi/wiki/Newcomers
[pip-installation]: https://pip.pypa.io/en/stable/installing/
[scanapi-examples]: https://github.com/scanapi/examples
[website]: https://scanapi.dev

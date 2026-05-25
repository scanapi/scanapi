# Quick Start

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
    width="700"
    alt="An overview screenshot of the report."
  >
  <img
    src="https://raw.githubusercontent.com/scanapi/scanapi/main/images/report-print-opened.png"
    width="700"
    alt="A screenshot of the report showing the request details."
  >
</p>

[pip-installation]: https://pip.pypa.io/en/stable/installing/

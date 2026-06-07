![](https://github.com/scanapi/design/raw/main/images/github-hero-dark.png)


#### Install with pipx (isolated CLI)


If `pip install scanapi` collides with the dependencies in your project's environment, install it with [pipx][pipx] instead. pipx gives ScanAPI its own virtual environment and still puts the `scanapi` command on your PATH:


```bash
$ pipx install scanapi
```


This is the recommended path when you want ScanAPI as a standalone CLI rather than a project dependency.


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


## Dependency Management


ScanAPI aims to minimize dependency conflicts and ensure a smooth developer experience. Most dependencies are specified as compatible version ranges to allow flexibility and avoid unnecessary conflicts. However, a few dependencies are strictly pinned for stability:


- **MarkupSafe==3.0.3**: Pinned to the latest version for security and compatibility. Relax if future versions are verified safe.
- **time-machine>=2.15.0**: time-machine is the actively maintained successor. Version range allows flexibility while ensuring compatibility.
- **requests-mock==1.12.1**: Pinned to the latest version for compatibility. Relax if future versions are verified safe.


All other dependencies use safe version ranges (e.g., `>=X.Y,<X+1.0`) to reduce the likelihood of dependency conflicts. If you encounter issues with dependency installation, please open an issue or PR.


Dependency updates are regularly reviewed to ensure compatibility with supported Python versions and CI stability.


## Contributing


Collaboration is super welcome! Check out our [contribution guide][contribution-guide] to get

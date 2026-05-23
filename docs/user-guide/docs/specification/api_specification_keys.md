# API Specification Keys

| KEY                  | Description                                                                                         | Type   | Scopes                            |
| -------------------- | --------------------------------------------------------------------------------------------------- | ------ | --------------------------------- |
| assert               | The test assertion                                                                                  | dict   | tests                             |
| body                 | The HTTP body of the request                                                                        | dict   | request                           |
| delay                | Performs a delay in milliseconds before each request call. (version >= 2.1.0)                       | int    | endpoint, request                 |
| endpoints            | Represents a list of API endpoints                                                                  | list   | endpoint                          |
| headers              | The HTTP headers                                                                                    | dict   | endpoint, request                 |
| max_retries          | A fixed maximum number of retries for a request before it is permanently failed. (version >= 2.2.0) | int    | retry                             |
| method               | The HTTP method of the request (GET, POST, PUT, PATCH or DELETE). If not set, GET will be used      | string | request                           |
| name                 | An identifier                                                                                       | string | endpoint, request, test           |
| params               | The HTTP query parameters                                                                           | dict   | endpoint, request                 |
| path                 | A part of the URL path that will be concatenated with possible other paths                          | string | endpoint, request                 |
| requests             | Represents a list of HTTP requests                                                                  | list   | endpoint                          |
| retry                | The retry configuration for a request. (Available for version >= 2.2.0)                             | dict   | request                           |
| tests                | Represents a list of tests to run against a HTTP response of a request                              | list   | request                           |
| vars                 | Key used to define your custom variables to be used along the specification                         | dict   | endpoint, request                 |
| ${custom var}        | Syntax to get the value of the custom variables defined at key `vars`                               | string | request - after `vars` definition |
| ${ENV_VAR}           | Syntax to get the value of an environment variable                                                  | string | endpoint, request                 |
| $\{\{python_code\}\} | Syntax to get the value of a Python code expression                                                 | string | request                           |

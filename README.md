# ScanAPI

A library for your API that provides:

- Automated Testing
- Automated Documentation

## How to install

```bash
$ pip install scanapi
```

## How to use

Create an API spec file `api.yaml` file in the root of your project and list the API's endpoints.

```yaml
api:
  base_url: https://jsonplaceholder.typicode.com/
  endpoints:
    - namespace: posts
      path: /posts
      requests:
        - name: list_all
          method: get
        - name: details
          method: get
          path: /1
```

To run the requests and create the doc, run:

```
$ scanapi --help
Usage: scanapi [OPTIONS]

  Automated Testing and Documentation for your REST API.

Options:
  -s, --spec-path PATH
  -d, --docs-path TEXT
  --help                Show this message and exit.
```

By default, the doc will be available in the `docs.md` file.

### Available Methods

You can run these methods:
- get
- post
- delete

### Configuration

If you want to configure scanapi, you can do it by creating a file `.scanapi.yaml` in the root of your project.

```yaml
spec_path: api.yaml
docs_path: docs.md
```

### Headers

```yaml
api:
  base_url: https://api.thecatapi.com/v1
  headers:
    x-api-key: DEMO-API-KEY
    Content-Type: application/json
  endpoints:
    - namespace: votes
      path: /votes
      requests:
        - name: list_all
          method: get
```

### Query Parameters

``` yaml
api:
  base_url: http://api.openweathermap.org/data/2.5
  params:
    APPID: <INSERT_YOUR_API_KEY_HERE>
  endpoints:
    - namespace: weather
      path: /weather
      requests:
        - name: city
          method: get
          params:
            q: Rio de Janeiro
```

### Body

In a post request you can add a body:

```yaml
api:
  base_url: https://api.thecatapi.com/v1
  headers:
    x-api-key: DEMO-API-KEY
    Content-Type: application/json
  endpoints:
    - namespace: votes
      path: /votes
      requests:
        - name: vote
          method: post
          body:
            image_id: asf2
            value: 1
            sub_id: demo-d4332e
```

### Environment Variables

You can use environment variables in your API spec file:

```yaml
api:
  base_url: ${BASE_URL}
  headers:
    Content-Type: application/json
  endpoints:
    - namespace: posts
      path: /posts
      requests:
        - name: list_all
          method: get
        - name: details
          method: get
          path: /1
```

And in the config file `.scanapi.yaml` set their values:

```yaml
env_vars:
  BASE_URL: https://jsonplaceholder.typicode.com/
```

### Chaining Requests

```yaml
api:
  base_url: https://jsonplaceholder.typicode.com/
  headers:
    Content-Type: application/json
  endpoints:
    - namespace: posts
      path: /posts
      requests:
        - name: list_all # posts_list_all
          method: get
          vars:
            post_id: ${{responses['posts_list_all'].json()[1]['id']}} # should return id 2
        - name: details # posts_details
          method: get
          path: ${post_id}
```

### Nested Endpoints

### Split API spec file in multiples files

To be implemented:

```
- api/
  - api.yaml
  - endpoints/
    - endpoints.yaml
    - posts/
      - posts.yaml
      - requests/
        - list-all.yaml
        - details.yaml
```

### Keys

| KEY               | Description                                                                                         | Type   | Scopes                            |
|-------------------|-----------------------------------------------------------------------------------------------------|--------|-----------------------------------|
| api               | It is reserver word that marks the root of the specification and must not appear in any other place | dict   | root                              |
| body              | The HTTP body of the request                                                                        | dict   | POST request                      |
| base_url          | The API’s base URL                                                                                  | string | api                               |
| endpoints         | It represents a list of API endpoints                                                               | list   | api, endpoint                     |
| headers           | The HTTP headers                                                                                    | dict   | api, endpoint, request            |
| method            | The HTTP method of the request                                                                      | string | request                           |
| name              | An identifier                                                                                       | string | endpoint, request                 |
| path              | A part of the URL path that will be concatenated with the base URL and possible other paths         | string | endpoint, request                 |
| requests          | It represents a list of HTTP requests                                                               | list   | api, endpoint                     |
| vars              | Key used to define your custom variables to be used along the specification                         | dict   | request                           |
| ${custom var}     | A syntax to get the value of the custom variables defined at key `vars`                             | string | request - after `vars` definition |
| ${ENV_VAR}        | A syntax to get the value of the environment variables defined at `.scanapi` file                   | string | api, endpoint, request            |
| ${{python_code}}  | A syntax to get the value of a Python code expression                                               | string | requests                          |

### Asserts

To be implemented

### Cases

To be implemented

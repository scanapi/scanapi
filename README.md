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

You can run this methods:
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
  base_url: https://jsonplaceholder.typicode.com/
  headers:
    Authorization: Bearer 3032196d-4563-4047-ac7b-e7763e43177e
  endpoints:
    - namespace: posts
      headers:
        Content-Type: application/json
      path: /posts
      requests:
        - name: list_all
          method: get
        - name: details
          method: get
          path: /1
```

### Params

``` yaml
api:
  base_url: http://api.openweathermap.org/data/2.5
  params:
    APPID: ${API_KEY}
  endpoints:
    - namespace: weather
      path: /weather
      requests:
        - name: city_weather
          method: get
          params:
            q: Rio de Janeiro
```

### Body

In a post request you can add a body:

```yaml
api:
  base_url: https://api.thecatapi.com/v1/votes
  headers:
    x-api-key: ${API_KEY} 
    Content-Type: application/json
  endpoints:
    - namespace: v1
      path: /v1
      requests:
        - name: votes
          method: post
          path: /votes
          body: 
            image_id: asf2
            value: 1
            sub_id: ${USER_ID}
```


### Cases

To be implemented

### Environment Variables

You can use environment variables in your API spec file:

```yaml
api:
  base_url: ${BASE_URL}
  headers:
    Authorization: ${BEARER_TOKEN}
  endpoints:
    - namespace: posts
      headers:
        Content-Type: application/json
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
  BEARER_TOKEN: Bearer 3032196d-4563-4047-ac7b-e7763e43177e
```

### Chaining Requests

```yaml
api:
  base_url: ${BASE_URL}
  headers:
    Authorization: ${BEARER_TOKEN}
  endpoints:
    - namespace: posts
      headers:
        Content-Type: application/json
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

### Asserts

To be implemented


### Automation with Peril

To be implemented

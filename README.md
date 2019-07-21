# API Scanner

A library for your API that provides:

- Automated Testing
- Automated Documentation

## How to install

To be implemented:

```bash
pip install api-scanner
```

## How to use

Create an API spec file `api.yaml` file in the root of your project and list the API's endpoints.

```yaml
api:
  base-url: https://jsonplaceholder.typicode.com/
  endpoints:
    - namespace: posts
      path: /posts
      requests:
        - name: list-all
          method: get
        - name: details
          method: get
          path: /1
```

To run the requests and create the doc, run:

```
python api-scanner.py
```

By default, the doc will be available in the `docs.md` file.

### Headers

```yaml
api:
  base-url: https://jsonplaceholder.typicode.com/
  headers:
    Authorization: Bearer 3032196d-4563-4047-ac7b-e7763e43177e
  endpoints:
    - namespace: posts
      headers:
        Content-Type: application/json
      path: /posts
      requests:
        - name: list-all
          method: get
        - name: details
          method: get
          path: /1
```

### Cases

To be implemented

### Chaining Requests

To be implemented

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

### Configuration

If you want to configure api-scanner, you can do it by creating a file `.api-scanner.yaml` in the root of your project.

```yaml
api-file: api.yaml
docs-file: docs.md
```

### Environment Variables

You can use environment variables in your API spec file:

```yaml
api:
  base-url: https://jsonplaceholder.typicode.com/
  headers:
    Authorization: ${env_bearer_token}
  endpoints:
    - namespace: posts
      headers:
        Content-Type: application/json
      path: /posts
      requests:
        - name: list-all
          method: get
        - name: details
          method: get
          path: ${env_post_id}
```

And in the config file `.api-scanner.yaml` set their values:

```yaml
env-vars:
  env_bearer_token: Bearer 3032196d-4563-4047-ac7b-e7763e43177e
  env_post_id: "/1"
```

### Automation with Peril

To be implemented

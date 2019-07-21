# API Scanner

A library for your API that provides:

- Automated Testing
- Automated Documentation

## How to install

```bash
pip install api-scanner
```

## How to use

Create an `api.yaml` file in the root of your project and list the API's endpoints.

```yaml
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

### Headers

```yaml
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

### Chaining Requests

### Split api.yaml in multiples files

### Asserts

### Configuration

If you want to configure api-scanner, you can do it by creating a file `.api-scanner.yaml` in the root of your project.

```yaml
api-file: api.yaml
docs-file: docs.md
```

### Environment Variables
### Automation with Peril

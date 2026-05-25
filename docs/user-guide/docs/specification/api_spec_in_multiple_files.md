# API Specification in Multiple Files

With `!include`, it is possible to build your API specification in multiple files.

For example, these two files

```yaml
# scanapi.yaml
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
endpoints:
  - name: scanapi-demo
    path: ${BASE_URL}
    requests:
      - name: health
        path: /health/
```

The same works for JSON specifications:

```jsonc
// scanapi.json
{
  "endpoints": [
    {
      "name": "scanapi-demo",
      "path": "${BASE_URL}",
      "requests": !include include.json
    }
  ]
}
```

```jsonc
// include.json
[
  {
    "name": "health",
    "path": "/health/"
  }
]
```

would generate:

```json
{
  "endpoints": [
    {
      "name": "scanapi-demo",
      "path": "${BASE_URL}",
      "requests": [
        {
          "name": "health",
          "path": "/health/"
        }
      ]
    }
  ]
}
```

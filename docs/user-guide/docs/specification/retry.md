# Retry

You can define a retry configuration for a request.

```yaml
requests:
  - name: my_request
    path: path/to/request
    retry:
      max_retries: 3
```

This means that ScanAPI will try a maximum of 3 times to make the request before it is permanently
failed.

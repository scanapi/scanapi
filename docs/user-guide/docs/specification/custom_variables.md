# Custom Variables

You can create custom variables using the syntax:

```yaml
requests:
  - name: my_request
    ...
    vars:
      my_variable_name: my_variable_value
```

And in the next requests you can access them using the syntax:


```yaml
${my_variable_name}
```

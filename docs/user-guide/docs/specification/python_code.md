# Python Code

You can add Python code to the API specification by using the syntax:

```yaml
{% raw %} ${{my_python_code}} {% endraw %}
```

For example

```yaml
body:
  uuid: 5c5af4f2-2265-4e6c-94b4-d681c1648c38
  name: Tarik
  yearsOfExperience: {% raw %} ${{2 + 5}} {% endraw %}
  languages:
    - ruby
      go
  newOpportunities: false
```

What I can use inside the {% raw %} `${{ }}` {% endraw %} syntax?
Any python code that **can run inside an `eval` python command**.
A short list of modules will be already available for you. They are all the imports of
[this file](https://github.com/scanapi/scanapi/blob/main/scanapi/evaluators/code_evaluator.py#L1).

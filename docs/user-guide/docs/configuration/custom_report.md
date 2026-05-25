# Custom Report

With ScanAPI you can create your own report template to show the results the way you prefer!
For that, the first step is to create a [Jinja template][jinja] file. The template can have the
extension you prefer: `.html`, `.md`, `.txt`, `.xml`...

## Template Context

Inside you template, you have some variables and methods which you can access to have ScanAPI
information.

### project_name

The project_name defined in the [Configuration File][config_file].

For example:

{% raw %}

```jinja
<header>
    {% if project_name %} {# when project_name is set in the config file #}
      <h1> Report generated for <span>{{ project_name }}</span></h1>
    {% else %} {# when project_name is not set in the config file #}
      <h1> Report generated for your API </h1>
    {% endif %}
</header>
```

{% endraw %}

### now

The current datetime

For example:

{% raw %}

```jinja
<p> Report Generated at: {{now}}</p>
```

{% endraw %}

### session

The object responsible to store the ScanAPI run information.

#### successes

The number of `test_results` that succeed in the session.

For example:

{% raw %}

```jinja
<span><strong>Number of PASSED:</strong> {{session.successes}}</span>
```

{% endraw %}

#### failures

The number of `test_results` that failed in the session.

For example:

{% raw %}

```jinja
<span><strong>Number of FAILURES:</strong> {{session.failures}}</span>
```

{% endraw %}

#### errors

The number of `test_results` that got an error in the session.

{% raw %}

```jinja
<span><strong>Number of ERRORS:</strong> {{session.errors}}</span>
```

{% endraw %}

#### exit_code

The exit code returned by the ScanAPI process.

{% raw %}

```jinja
<span>The script returned the exit code: <strong>{{session.exit_code}}</strong></span>
```

{% endraw %}

#### started_at

The datetime when ScanAPI started to run.

```jinja
{% raw %}<span><strong>Started at: </strong> {{ session.started_at }}</span>{% endraw %}
```

#### elapsed_time()

The elapsed time since the session started.

{% raw %}

```jinja
<span><strong>Total Time:</strong> {{ session.elapsed_time() }}</span>
```

{% endraw %}

### results

A [generator object][generator] containing results for each request. Each result contains the
information for a request.

{% raw %}

```jinja
{% for result in results -%}
...
{% endfor %}
```

{% endraw %}

#### response

The [Response object][requests_response] which contains the server’s response to the HTTP request.

{% raw %}

```jinja
{% for result in results -%}
  {% set response = result.response %}
  {% set request = response.request %}

  <p>Full URL: <a href="{{request.url}}"> {{request.url}}</a></p>
  <p>Response Status Code: <span>{{ response.status_code }}</span></p>
{% endfor %}
```

{% endraw %}

#### no_failure

A boolean that indicates if the tests for the request didn't get any failure. True if there are no
failures or errors. False if there is any failure or error.

{% raw %}

```jinja
{% for result in results -%}
  {% set endpoint_status_label = "PASS" if result.no_failure else "FAIL" %}

  <p>Status: <span>{{ endpoint_status_label }}</span></p>
{% endfor %}
```

{% endraw %}

#### tests_results

A list object containing the results for each test. Each result contains the information of a
test for the request.

{% raw %}

```jinja
{% for result in results -%}
  {% set tests = result.tests_results %}

  {% for test in tests -%}
    ...
  {% endfor %}
{% endfor %}
```

{% endraw %}

##### name

The name of the test defined in the API specification.

{% raw %}

```jinja
{% for result in results -%}
  {% set tests = result.tests_results %}

  {% for test in tests -%}
    <p>Test Name: <span>{{ test.name }}</span></p>
  {% endfor %}
{% endfor %}
```

{% endraw %}

##### status

The status of the test result. One of the values: `"passed"`, `"failed` or `"error"`.

{% raw %}

```jinja
{% for result in results -%}
  {% set tests = result.tests_results %}

  {% for test in tests -%}
    <p>Test Name: <span>{{ test.name }}</span></p>
    <p>Test Status: <span>{{test.status|upper}}</span></p>
  {% endfor %}
{% endfor %}
```

{% endraw %}

##### failure

The assertion sentence that failed. It will be empty if there is no failure.

{% raw %}

```jinja
{% for result in results -%}
  {% set tests = result.tests_results %}

  {% for test in tests -%}
    <p>Test Name: <span>{{ test.name }}</span></p>
    <p>Test Status: <span>{{test.status|upper}}</span></p>
    {% if test.failure %}
      <span>{{test.failure}} is false</span>
    {% endif %}
  {% endfor %}
{% endfor %}
```

{% endraw %}

##### error

The exception thrown in the test. It will be empty if there is no error.

{% raw %}

```jinja
{% for result in results -%}
  {% set tests = result.tests_results %}

  {% for test in tests -%}
    <p>Test Name: <span>{{ test.name }}</span></p>
    <p>Test Status: <span>{{test.status|upper}}</span></p>
    {% if test.error %}
      <span>An error occurred: {{test.error}}</span>
    {% endif %}
  {% endfor %}
{% endfor %}
```

{% endraw %}

## Running ScanAPI with Custom Report

After creating your report template, now you can run ScanAPI using it. For example:

```shell
$ scanapi run -t my_template.html
```

And that is it! Now ScanAPI will use you custom template `my_template.html` instead of the default
one.

Also, if you want to check, this is the [default template code][default_template], it might help
you!

[config_file]: config_file.md
[default_template]: https://github.com/scanapi/scanapi/blob/main/scanapi/templates/report.html
[generator]: https://wiki.python.org/moin/Generators
[jinja]: https://jinja.palletsprojects.com/en/2.11.x/
[requests_response]: https://docs.python-requests.org/en/latest/api/#requests.Response

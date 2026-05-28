# Custom Report

ScanAPI enables you to generate personalized reports. With the [Custom Report][doc-custom-report]
feature, you can export your results in any style and format you want
(`.html`, `.md`, `.txt`, `.xml`...).

Let's export your ScanAPI results you have so far as a `.csv` file. For that, the first step is
to create a [Jinja template][jinja] file. Create a `csv_template.jinja` file in root with the
following content:

```jinja
{% raw %}"project_name"{{- "," -}}
"generated_at"{{- "," -}}
"total_successes"{{- "," -}}
"total_failures"{{- "," -}}
"total_errors"{{- "," -}}
"started_at"{{- "," -}}
"total_time"{{- "," -}}
"url"{{- "," -}}
"all_tests_passed"{{- "," -}}
"test_name"
{% for result in results -%}
{% for test in result.tests_results -%}
    "{{ project_name }}"{{- "," -}}
    "{{ now }}"{{- "," -}}
    {{ session.successes }}{{- "," -}}
    {{ session.failures }}{{- "," -}}
    {{ session.errors }}{{- "," -}}
    "{{ session.started_at }}"{{- "," -}}
    "{{ session.elapsed_time() }}"{{- "," -}}
    "{{ result.response.request.url }}"{{- "," -}}
    {{ result.no_failure }}{{- "," -}}
    "{{ test.name }}"
{% endfor %}
{%- endfor %}{% endraw %}
```

The folder structure should look like this now:

```
- scanapi (root directory)
|── .env
|── csv_template.jinja
|── scanapi-report.html
|── scanapi.conf
|── scanapi.yaml
|___  snippets.yaml
```

Let's run ScanAPI using the new csv template and save the results in the `scanapi-report.csv` file:

```shell
$ scanapi run -t csv_template.jinja -o scanapi-report.csv
```

The `.csv` result:

<p align="center">
  <img
    src="/assets/images/tutorial/step12/report-csv.png"
    width="900"
    alt="CSV Report"
  >
</p>

This should be the final folder structure:

```
- scanapi (root directory)
|── .env
|── csv_template.jinja
|── scanapi-report.csv
|── scanapi-report.html
|── scanapi.conf
|── scanapi.yaml
|___  snippets.yaml
```

Congratulations, you have finished documenting and testing the Snippets API using ScanAPI! 🎉

Great, but it is still missing one last piece. How can I add ScanAPI to my own API? How can I add
ScanAPI to my project and to my pipeline? Let's go to our final lesson!

[doc-custom-report]: ../docs/configuration/custom_report.md
[jinja]: https://jinja.palletsprojects.com/en/2.11.x/

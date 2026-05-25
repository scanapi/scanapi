# Project Name

You can add a title to your report, this way you can easily differentiate reports from different
APIs. To do so, we need to set the `project_name` in the configuration file `scanapi.conf`:

```yaml
project_name: Snippets API
```

Putting it all together:

```yaml
project_name: Snippets API
report:
  hide_request:
    body:
      - password
    headers:
      - Authorization
  hide_response:
    body:
      - key
```

Run ScanAPI again and reload the report:

```shell
$ scanapi run
```

<p align="center">
  <img
    src="/assets/images/tutorial/step11/report-1.png"
    width="900"
    alt="Report overview - project name"
  >
</p>

You can check all the possible settings you can set for your project at our
[Configuration File Doc][doc-config-file].

Ok, but what if you don't like the style of our report? Or if some information you'd like to see is
missing? Or even if you need the report in another format other than html? Don't worry, let's see
how can you create your own ScanAPI report.

[doc-config-file]: ../docs/configuration/config_file.md

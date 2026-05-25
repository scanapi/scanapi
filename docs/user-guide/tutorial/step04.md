# Writing Tests

It is time to test the response you received. Change your specification file `scanapi.yaml` to have
the following content:

```yaml
{% raw %}endpoints:
  - name: snippets-api
    path: https://demo.scanapi.dev/api/v1/
    headers:
      Content-Type: application/json
    requests:
      - name: health
        method: get
        path: /health/
        tests: # this is new
          - name: status_code_is_200 # this is new
            assert: ${{ response.status_code == 200 }} # this is new
          - name: body_equals_ok # this is new
            assert: ${{ response.json() == "OK!" }} {% endraw %} # this is new
```

Run ScanAPI again:

```shell
$ scanapi run
```

Reload your browser and check the `TESTS` now:

<p align="center">
  <img
    src="/assets/images/tutorial/step04/report-tests.png"
    width="900"
    alt="Test details"
  >
</p>

Inside the {% raw %} `${{ }}` {% endraw %} notation, you can write pure [Python Code][python-code].
`response` is a [requests.Response][requests-response] object containing the response information
of the request.

Note that the `Tests Summary` brings some useful information about the tests now.
If anything goes wrong or if any test fails, `scanapi` command will return an error with the
corresponding exit code.

<p align="center">
  <img
    src="/assets/images/tutorial/step04/report-tests-summary.png"
    width="900"
    alt="Tests summary"
  >
</p>

Congrats, you have documented and tested your first request! Now, it is time to start testing
endpoints that need authentication.

[python-code]: ../docs/specification/python_code.md
[requests-response]: https://docs.python-requests.org/en/latest/api/#requests.Response

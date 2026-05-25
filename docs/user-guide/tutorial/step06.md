# Hiding Sensitive Information

We need to configure ScanAPI in order to
[hide the sensitive information][docs-hide-sensitive-info] of `/login` in our report.
Create a configuration file `scanapi.conf` in root directory with the following content:

```yaml
report:
  hide_request:
    body:
      - password
  hide_response:
    body:
      - key
```

The folder structure should look like this now:

```
- scanapi (root directory)
|── .env
|── scanapi-report.html
|── scanapi.conf
|___  scanapi.yaml
```

Let's run ScanAPI again and reload the report:

```shell
$ scanapi run
```

<p align="center">
  <img
    src="/assets/images/tutorial/step06/report-1.png"
    width="900"
    alt="Hidden Credentials"
  >
</p>

<p align="center">
  <img
    src="/assets/images/tutorial/step06/report-2.png"
    width="900"
    alt="Hidden key"
  >
</p>

Note that all sensitive fields are properly hidden now. Great, so let's make some authenticated
requests using the **Authentication Token** you received in the `/login` response.

[docs-hide-sensitive-info]: ../docs/configuration/hiding_sensitive_information.md

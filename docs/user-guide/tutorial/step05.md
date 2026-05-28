# Environment Variables (env vars)

Once you have already [register an user][docs-sign-up] for the Snippets API, you can test and
document the `/login` request.

It is not secure to explicitly write your API's username and password in a plain text.
For this reason, let's use [environment variables][env-var-definition].

## Setting Env Vars

Let's set your env vars:

```shell
$ export USER=<your_snippets_api_username_here>
$ export PASSWORD=<your_snippets_api_password_here>
```

The username and the password should be the ones you registered in the
[API Sign Up page][docs-sign-up]. Example:

```shell
$ export USER=my_user
$ export PASSWORD=XpoCDR36EPQxF5M
```

Your environment variables will be available in this terminal section. You can check them by
running:

```shell
$ echo $USER
my_user
$ echo $PASSWORD
XpoCDR36EPQxF5M
```

Note, if you close this terminal section, you will need to export the variables again. To make this
job a bit less manual, let's create a file to store these values. Create an `.env` file in root with
the following content:

```shell
export USER=my_user
export PASSWORD=XpoCDR36EPQxF5M
```

The folder structure should look like this now:

```
- scanapi (root directory)
|── .env
|── scanapi-report.html
|___  scanapi.yaml
```

Every time you need to load your env vars again, you can just run:

```shell
$ source .env
```

> Do not commit your `.env` file, it should not be added to the version control.
> To avoid any future mistakes, make sure to add `.env` to `.gitignore` so no-one accidentally
> pushes the `.env` containing secrets to the repository.

## Using Env Vars

It is time to use the exported env vars in the ScanAPI specification in order to access `/login`.
In the `scanapi.yaml` file, add the `get_token` request:

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
        tests:
          - name: status_code_is_200
            assert: ${{ response.status_code == 200 }}
          - name: body_equals_ok
            assert: ${{ response.json() == "OK!" }}
      - name: get_token # this is new
        path: /rest-auth/login/ # this is new
        method: post # this is new
        body: # this is new
          username: ${USER} # this is new
          password: ${PASSWORD}{% endraw %} # this is new
```

Using the [env var notation][docs-env-vars], ScanAPI will be able to access the exported values of
each variable. Let's run ScanAPI again and reload the report:

```shell
$ scanapi run
```

The result seems fine, the status code of the response is 200 and the login was complete
successfully.

<p align="center">
  <img
    src="/assets/images/tutorial/step05/report-1.png"
    width="900"
    alt="Report overview"
  >
</p>

But, if we look closer, the report is showing your secret information:

<p align="center">
  <img
    src="/assets/images/tutorial/step05/report-2.png"
    width="900"
    alt="Exposed Credentials"
  >
</p>

Besides, the response content also contains sensitive information that is being exposed:

<p align="center">
  <img
    src="/assets/images/tutorial/step05/report-3.png"
    width="900"
    alt="Exposed Key"
  >
</p>

Let's see how we can hide these values.

[env-var-definition]: https://en.wikipedia.org/wiki/Environment_variable
[docs-env-vars]: ../docs/specification/environment_variables.md
[docs-sign-up]: ./step02.md

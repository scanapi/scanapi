# Chaining Requests

Let's create your first code snippet! In the `scanapi.yaml` file, add the `create_snippet` request:

```yaml
{% raw %}- name: create_snippet
  path: /snippets/
  method: post
  body:
    title: Hello World
    code: "print('hello world')"
    style: "xcode"
    language: "python"
  tests:
    - name: status_code_is_201
      assert: ${{ response.status_code == 201 }}{% endraw %}
```

Putting it all together:

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
      - name: get_token
        path: /rest-auth/login/
        method: post
        body:
          username: ${USER}
          password: ${PASSWORD}

      # ALL BELOW IS NEW
      - name: create_snippet
        path: /snippets/
        method: post
        body:
          title: Hello World
          code: "print('hello world')"
          style: "xcode"
          language: "python"
        tests:
          - name: status_code_is_201
            assert: ${{ response.status_code == 201 }}{% endraw %}
```

Run ScanAPI again and reload the report:

```shell
$ scanapi run
```

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-1.png"
    width="900"
    alt="Report overview - failing"
  >
</p>

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-2.png"
    width="900"
    alt="Failing test"
  >
</p>

Oops, the response is Unauthorized. That makes the test fail and also, we could not create the
snippet code. To fix it, we need to send the **Authentication Token** received in the `/login`
response in the Authorization headers of `/snippets`.

In the `scanapi.yaml` file, in the `get_token` request, let's store the received key in the `token`
variable:

```yaml
{% raw %}vars:
  token: ${{response.json()["key"]}}{% endraw %}
```

and in the `create_snippet` request, let's send the token in via `Authorization` header:

```yaml
{% raw %}headers:
  Authorization: Token ${token}{% endraw %}
```

Putting it all together:

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
      - name: get_token
        path: /rest-auth/login/
        method: post
        body:
          username: ${USER}
          password: ${PASSWORD}
        vars: # this is new
          token: ${{response.json()["key"]}} # this is new
      - name: create_snippet
        path: /snippets/
        method: post
        headers: # this is new
          Authorization: Token ${token} # this is new
        body:
          title: Hello World
          code: "print('hello world')"
          style: "xcode"
          language: "python"
        tests:
          - name: status_code_is_201
            assert: ${{ response.status_code == 201 }}{% endraw %}
```

Run ScanAPI again and reload the report

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-3.png"
    width="900"
    alt="Report overview - success"
  >
</p>

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-4.png"
    width="900"
    alt="Response details"
  >
</p>

It works now! But, it is still missing one detail. Your key is being exposed in the request details

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-5.png"
    width="900"
    alt="Request details - exposed key"
  >
</p>

Let's also hide this information. Add the `Authorization` `headers` to the `hide_request` in the
`scanapi.conf`:

```yaml
report:
  hide_request:
    body:
      - password
    headers: # this is new
      - Authorization # this is new
  hide_response:
    body:
      - key
```

Run ScanAPI and reload the report again

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-6.png"
    width="900"
    alt="Request details - hidden key"
  >
</p>

All good, the sensitive information is hidden now. Using the same idea, lets chain dynamically one
more request. In the `scanapi.yaml` file, in the `create_snippet` request, let's store the `id` of
the created snippet:

```yaml
{% raw %}vars:
  snippet_id: ${{response.json()["id"]}}{% endraw %}
```

and let's create a new request to get the details of your brand new snippet:

```yaml
{% raw %}- name: snippet_details
  path: /snippets/${snippet_id}/
  method: get
  tests:
    - name: status_code_is_200
      assert: ${{ response.status_code == 200 }}{% endraw %}
```

Putting it all together:

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
      - name: get_token
        path: /rest-auth/login/
        method: post
        body:
          username: ${USER}
          password: ${PASSWORD}
        vars:
          token: ${{response.json()["key"]}}
      - name: create_snippet
        path: /snippets/
        method: post
        headers:
          Authorization: Token ${token}
        body:
          title: Hello World
          code: "print('hello world')"
          style: "xcode"
          language: "python"
        vars: # this is new
          snippet_id: ${{response.json()["id"]}} # this is new
        tests:
          - name: status_code_is_201
            assert: ${{ response.status_code == 201 }}
      - name: snippet_details # this is new
        path: /snippets/${snippet_id}/ # this is new
        method: get # this is new
        tests: # this is new
          - name: status_code_is_200 # this is new
            assert: ${{ response.status_code == 200 }} # this is new{% endraw %}
```

Run ScanAPI again and reload the report

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-7.png"
    width="900"
    alt="Report overview - snippet details"
  >
</p>

Let's go ahead and add more snippet requests:

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
      - name: get_token
        path: /rest-auth/login/
        method: post
        body:
          username: ${USER}
          password: ${PASSWORD}
        vars:
          token: ${{response.json()["key"]}}
      - name: create_snippet
        path: /snippets/
        method: post
        headers:
          Authorization: Token ${token}
        body:
          title: Hello World
          code: "print('hello world')"
          style: "xcode"
          language: "python"
        vars:
          snippet_id: ${{response.json()["id"]}}
        tests:
          - name: status_code_is_201
            assert: ${{ response.status_code == 201 }}
      - name: snippet_details
        path: /snippets/${snippet_id}/
        method: get
        tests:
          - name: status_code_is_200
            assert: ${{ response.status_code == 200 }}

      # ALL BELOW IS NEW
      - name: snippet_update_with_patch
        path: /snippets/${snippet_id}/
        method: patch
        headers:
          Authorization: Token ${token}
        body:
          code: "print('hello, patch')"
        tests:
          - name: status_code_is_200
            assert: ${{ response.status_code == 200 }}
      - name: snippet_update_with_put
        path: /snippets/${snippet_id}/
        method: put
        headers:
          Authorization: Token ${token}
        body:
          title: Hello World - Ruby
          code: "puts 'hello world'"
          style: "emacs"
          language: "ruby"
        tests:
          - name: status_code_is_200
            assert: ${{ response.status_code == 200 }}
      - name: delete_snippet
        path: snippets/${snippet_id}/
        method: delete
        headers:
          Authorization: Token ${token}
        tests:
          - name: status_code_is_204
            assert: ${{ response.status_code == 204 }}
      - name: snippets_list_all
        path: /snippets/
        method: get
        tests:
          - name: status_code_is_200
            assert: ${{ response.status_code == 200 }}{% endraw %}
```

Run ScanAPI again and reload the report

<p align="center">
  <img
    src="/assets/images/tutorial/step07/report-8.png"
    width="900"
    alt="Report overview - snippet details"
  >
</p>

Yay, you have finished testing and documenting the snippets requests using ScanAPI! 🎉

With the [chaining requests feature][docs-chaining-requests], you can use any responses information
from one request into the next requests via [custom variables][docs-custom-variables]. This gives
you huge flexibility and the power to test complex scenarios.

You might have noticed that the specification has a lot of repeated code. Let's see how we can
improve it using nested endpoints.

[docs-chaining-requests]: ../docs/specification/chaining_requests.md
[docs-custom-variables]: ../docs/specification/custom_variables.md

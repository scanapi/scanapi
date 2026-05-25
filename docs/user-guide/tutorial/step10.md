# Include

Using the `!include` notation, you can [split your specification into multiples files][docs-include].
Let's extract the `snippets` endpoint to a separated file. Create `snippets.yaml` in root with
the following content:

```yaml
{% raw %}name: snippets
path: snippets/
headers:
  Authorization: Token ${token}
requests:
  - name: create
    method: post
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
  - name: details
    path: ${snippet_id}/
    tests:
      - name: status_code_is_200
        assert: ${{ response.status_code == 200 }}
  - name: update_with_patch
    path: ${snippet_id}/
    method: patch
    body:
      code: "print('hello, patch')"
    tests:
      - name: status_code_is_200
        assert: ${{ response.status_code == 200 }}
  - name: snippet_update_with_put
    path: ${snippet_id}/
    method: put
    body:
      title: Hello World - Ruby
      code: "puts 'hello world'"
      style: "emacs"
      language: "ruby"
    tests:
      - name: status_code_is_200
        assert: ${{ response.status_code == 200 }}
  - name: delete
    path: ${snippet_id}/
    method: delete
    tests:
      - name: status_code_is_204
        assert: ${{ response.status_code == 204 }}
  - name: list_all
    tests:
      - name: status_code_is_200
        assert: ${{ response.status_code == 200 }}{% endraw %}
```

And, let's replace all the `snippets` endpoint code in the `scanapi.yaml` by:

```yaml
{% raw %} !include snippets.yaml {% endraw %}
```

The file `scanapi.yaml` should look like this now:

```yaml
{% raw %} endpoints:
  - name: snippets-api
    path: https://demo.scanapi.dev/api/v1/
    headers:
      Content-Type: application/json
    requests:
      - name: health
        path: health/
        tests:
          - name: status_code_is_200
            assert: ${{ response.status_code == 200 }}
          - name: body_equals_ok
            assert: ${{ response.json() == "OK!" }}
      - name: get_token
        path: rest-auth/login/
        method: post
        body:
          username: ${USER}
          password: ${PASSWORD}
        vars:
          token: ${{response.json()["key"]}}
    endpoints:
      - !include snippets.yaml {% endraw %}
```

Also, this should be the folder structure:

```
- scanapi (root directory)
|── .env
|── scanapi-report.html
|── scanapi.conf
|── scanapi.yaml
|___  snippets.yaml
```

Worth noticing that you can recursively include files. In our example, the `snippets.yaml` could be
composed of as many includes as you want.

Awesome, the code is way more clean now. The next step is to add a title to your report!

[docs-include]: ../docs/specification/api_spec_in_multiple_files.md

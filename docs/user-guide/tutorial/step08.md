# Nested Endpoints

In the ScanAPI specification, each `endpoint` can have multiple endpoints nested into it.
This feature makes it possible to aggregate requests that have the same route below the same
endpoint. All the common attributes can be applied directly to the endpoint and they will be
propagated to the endpoint's children recursively.

Let's see how we could rewrite our specification file `scanapi.yaml` using nested endpoints:

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
    endpoints:
      - name: snippets
        path: /snippets
        headers:
          Authorization: Token ${token}
        requests:
          - name: create
            path: /
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
            path: /${snippet_id}/
            method: get
            tests:
              - name: status_code_is_200
                assert: ${{ response.status_code == 200 }}
          - name: update_with_patch
            path: /${snippet_id}/
            method: patch
            body:
              code: "print('hello, patch')"
            tests:
              - name: status_code_is_200
                assert: ${{ response.status_code == 200 }}
          - name: update_with_put
            path: /${snippet_id}/
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
            path: /${snippet_id}/
            method: delete
            tests:
              - name: status_code_is_204
                assert: ${{ response.status_code == 204 }}
          - name: list_all
            path: /
            method: get
            tests:
              - name: status_code_is_200
                assert: ${{ response.status_code == 200 }}
{% endraw %}
```

Note that every attribute from the parent propagates to its children. The Authorization header, for
example, was only declared at the snippet endpoint level, but it propagates to all its requests.
The same happens with the `path`. Declaring `/snippets` in the parent makes that all the children
have this path concatenated to its URL.

If you run ScanAPI again and reload the report, the results should be similar as before. Awesome,
we have already reached a better result. Still, we can keep improving on it. Let's see how we can
refactor the code using the ScanAPI default values.

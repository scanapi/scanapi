# Default Values

By default, the request method is `get`, so we can go ahead and remove all `method: get` from our
spec.

```yaml
{% raw %}endpoints:
  - name: snippets-api
    path: https://demo.scanapi.dev/api/v1/
    headers:
      Content-Type: application/json
    requests:
      - name: health
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
        - name: snippet_update_with_put
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
          tests:
            - name: status_code_is_200
              assert: ${{ response.status_code == 200 }}{% endraw %}
```

Also, `path` is not mandatory for a request. If you don't want to concatenate anything in the
endpoint path, you can skip it. Let's remove all `path: /` from our spec.

```yaml
{% raw %}endpoints:
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
      - name: snippets
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

Great, they are small changes that make the specification a bit cleaner. Let's see how can we have
a huge readability improvement by splitting the specification file in multiple files.

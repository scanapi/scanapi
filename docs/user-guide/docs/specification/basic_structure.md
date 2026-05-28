# Basic Structure

You can write ScanAPI specifications in YAML or JSON. In this guide, we use only YAML examples but JSON works equally well.

A sample ScanAPI specification written in YAML looks like:

```yaml
endpoints:
  - name: sample-api
    path: http://api.example.com/v1
    requests:
      - name: users
        path: /users
        method: get
        tests:
          - name: status_code_is_200
            assert: {% raw %} ${{ response.status_code == 200 }} {% endraw %}
```

This specification follows a tree structure.

One value defined in a node will propagate to it's children, concatenating the values.

In the example above, for instance, the final path of the request will be:

```
http://api.example.com/v1/users
```

Which is a result of the concatenation of the **sample-api** endpoint path `http://api.example.com/v1` with the **users** request path `/users`.

```
http://api.example.com/v1 (sample-api endpoint path) + /users (users request path)
```

## Endpoints Section

The `endpoints` key represents a new tree branch, in the form of a list. The purpose of an endpoint is to aggregate common properties of requests. You can append as many endpoints as you like.

```
endpoint = non-leaf node
request = leaf
```

### Available keys

Each item of the endpoints list has the following keys available:

- \- delay
- \- endpoints
- \- headers
- \- name
- \- params
- \- path
- \- requests
- \- vars

## Requests Section

The requests section represents a list of HTTP requests. Inside a request it will also be defined the expected behavior of its response.

Requests can only be defined under an endpoint.

### Available keys

Each item of the requests list has the following keys available:

- \- body
- \- delay
- \- headers
- \- method
- \- name
- \- params
- \- path
- \- retry
- \- tests
- \- vars

## Retry Section

The retry section is where it will be defined the retry configuration for a request.

### Available keys

- \- max_retries

## Tests Section

The tests section is where it will be defined the tests for a request.

### Available keys

Each item of the tests list has the following keys available:

- \- assert
- \- name

# Specification keys

## assert

Is the actual test statement. It describes the expected behavior for a response.

type: string
syntax: python code

## body

The content that will be sent as the HTTP request body.

type: dict

## delay

The time in milliseconds to perform a delay before each request call. (Available for version >= 2.1.0)

type: int

## endpoints

It is the key word for the [endpoints section](#endpoints-section).

type: list

## headers

The content that will be sent as the HTTP request header.

type: dict

## max_retries

A fixed maximum number of retries for a request before it is permanently failed.

type: int

## method

The HTTP method for the request. Currently the supported methods are GET, POST, PUT, PATCH and DELETE.

type: string

## name

A identifier for the current resource (endpoint, request or test).

type: string

## params

The HTTP query parameters.

type: dict

## path

The request URL.

type: string

## requests

It is the key word for the [requests section](#requests-section).

type: list

## retry

It is the key word for the [retry section](#retry-section).

type: dict

## tests

It is the key word for the [tests section](#tests-section).

type: list

## vars

Key used to define your custom variables to be used along the specification.

Read more about [custom variables](custom_variables.md).

type: dict

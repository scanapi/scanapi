# Chaining Requests

Inside the request scope, you can save the results of the response to use in the next
requests. For example:

```yaml
requests:
  - name: list_all
    method: get
    vars:
      dev_id: {% raw %} ${{response.json()[2]["uuid"]}} {% endraw %}
```

The dev_id variable will receive the `uuid` value of the 3rd result from the devs_list_all request

If the response is

```json
[
    {
        "uuid": "68af402f-1084-40a4-b9b2-6bb5c2d11559",
        "name": "Anna",
        "yearsOfExperience": 5,
        "languages": [
            "python",
            "c"
        ],
        "newOpportunities": true
    },
    {
        "uuid": "0d1bd106-c585-4d6b-b3a4-d72dedf7190e",
        "name": "Louis",
        "yearsOfExperience": 3,
        "languages": [
            "java"
        ],
        "newOpportunities": true
    },
    {
        "uuid": "129e8cb2-d19c-41ad-9921-cea329bed7f0",
        "name": "Marcus",
        "yearsOfExperience": 4,
        "languages": [
            "c"
        ],
        "newOpportunities": false
    }
]
```

The dev_id variable will receive the value `129e8cb2-d19c-41ad-9921-cea329bed7f0`

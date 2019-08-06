#!/usr/bin/env python3
import requests
import yaml

from scanapi.api_node import APINode, RequestNode
from scanapi.variable_parser import save_response


class RequestsBuilder:
    ALLOWED_HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")

    def __init__(self, api_spec):
        if "api" not in api_spec:
            print("API spec must start with api key as root")

        self.api_spec = api_spec["api"]
        self.requests = []

    def build_all(self):
        root = APINode(self.api_spec)

        if not "endpoints" in self.api_spec:
            return self.build_requests(root)

        return self.build_endpoints(root)

    def call_all(self):
        responses = []

        for request in self.requests:
            request.evaluate_request()
            response = self.make_request(request)
            save_response(request.id, response)
            responses.append(response)

            request.save_custom_vars()

        return responses

    def build_endpoints(self, parent):
        for endpoint_spec in parent.spec["endpoints"]:
            endpoint = APINode(endpoint_spec, parent)
            self.build_requests(endpoint)

            if "endpoints" in endpoint.spec:
                self.build_endpoints(endpoint)

    def build_requests(self, endpoint):
        for request_spec in endpoint.spec["requests"]:
            self.requests.append(RequestNode(request_spec, endpoint))

    def make_request(self, request):
        method = request.method.upper()

        if method not in self.ALLOWED_HTTP_METHODS:
            print(
                "HTTP method not supported: {}. Supported methods: {}. Request ID: {}".format(
                    method, self.ALLOWED_HTTP_METHODS, request.id
                )
            )
            return

        return requests.request(
            method,
            request.url,
            headers=request.headers,
            params=request.params,
            json=request.body,
        )

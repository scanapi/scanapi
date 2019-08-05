#!/usr/bin/env python3
import requests
import yaml

from scanapi.api_node import APINode, RequestNode
from scanapi.variable_parser import save_response


class RequestsBuilder:
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
            if request.spec["method"].lower() == "get":
                response = self.get_request(
                    request.url, request.headers, request.params
                )
                response_id = "{}_{}".format(request.namespace, request.spec["name"])
                save_response(response_id, response)
                responses.append(response)

            if request.spec["method"].lower() == "post":
                response = self.post_request(
                    request.url, request.headers, request.body, request.params
                )
                response_id = "{}_{}".format(request.namespace, request.spec["name"])
                save_response(response_id, response)
                responses.append(response)

            if request.spec["method"].lower() == "delete":
                response = self.delete_request(
                    request.url, request.headers, request.body, request.params
                )
                response_id = "{}_{}".format(request.namespace, request["name"])
                save_response(response_id, response)
                responses.append(response)

            request.save_custom_vars()

        return responses

    def build_endpoints(self, parent):
        for endpoint_spec in parent.spec["endpoints"]:
            endpoint = APINode(endpoint_spec, parent)
            self.build_requests(endpoint)

            if "endpoints" in endpoint.spec:
                return self.build_endpoints(endpoint)

    def build_requests(self, endpoint):
        for request_spec in endpoint.spec["requests"]:
            self.requests.append(RequestNode(request_spec, endpoint))

    def get_request(self, url, headers, params):
        return requests.get(url, headers=headers, params=params)

    def post_request(self, url, headers, body, params):
        return requests.post(url, json=body, headers=headers, params=params)

    def delete_request(self, url, headers, body, params):
        return requests.delete(url, headers=headers, json=body, params=params)

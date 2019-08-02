#!/usr/bin/env python3
import requests
import yaml

from scanapi.api_node import APINode, RequestNode
from scanapi.variable_parser import populate_dict, populate_str, save_response


class RequestsBuilder:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as stream:
            try:
                self.api = yaml.safe_load(stream)["api"]
            except yaml.YAMLError as exc:
                print(exc)

    def call_all(self):
        root = APINode(self.api)

        return self.call_endpoints(root)

    def call_endpoints(self, parent):
        responses = []

        for endpoint_spec in parent.spec["endpoints"]:
            endpoint = APINode(endpoint_spec, parent)
            responses = responses + self.call_requests(endpoint)

            if "endpoints" in endpoint.spec:
                return self.call_endpoints(endpoint)

        return responses

    def call_requests(self, endpoint):
        responses = []
        for request_spec in endpoint.spec["requests"]:
            request = RequestNode(request_spec, endpoint)

            if request_spec["method"].lower() == "get":
                response = self.get_request(
                    request.url, request.headers, request.params
                )
                response_id = "{}_{}".format(request.namespace, request_spec["name"])
                save_response(response_id, response)
                responses.append(response)

            if request_spec["method"].lower() == "post":
                response = self.post_request(request.url, request.headers, request.body)
                response_id = "{}_{}".format(request.namespace, request_spec["name"])
                save_response(response_id, response)
                responses.append(response)

            request.save_custom_vars()

        return responses

    def get_request(self, url, headers, params):
        return requests.get(url, headers=headers, params=params)

    def post_request(self, url, headers, body):
        return requests.post(url, json=body, headers=headers)

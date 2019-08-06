#!/usr/bin/env python3
import click
import logging
import requests
import yaml

from scanapi.api_node import APINode, RequestNode
from scanapi.errors import HTTPMethodNotAllowedError, APIKeyMissingError
from scanapi.variable_parser import save_response

logger = logging.getLogger(__name__)


class RequestsBuilder:
    ALLOWED_HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")

    def __init__(self, api_spec):
        if "api" not in api_spec:
            raise APIKeyMissingError

        self.api_spec = api_spec["api"]
        self.requests = []

    def build_all(self):
        logger.info("Building requests")
        root = APINode(self.api_spec)

        if not "endpoints" in self.api_spec:
            return self.build_requests(root)

        return self.build_endpoints(root)

    def call_all(self):
        responses = []

        for request in self.requests:
            request.evaluate_request()
            try:
                response = self.make_request(request)
            except Exception as e:
                error_message = "Error to make request {}".format(request.id)
                error_message = "{} {}".format(error_message, str(e))
                logger.error(error_message)
                continue
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
            raise HTTPMethodNotAllowedError(method, self.ALLOWED_HTTP_METHODS)

        return requests.request(
            method,
            request.url,
            headers=request.headers,
            params=request.params,
            json=request.body,
        )

#!/usr/bin/env python3
import click
import logging
import requests
import yaml

from scanapi.errors import HTTPMethodNotAllowedError


logger = logging.getLogger(__name__)


class RequestsMaker:
    ALLOWED_HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")

    def __init__(self, api_tree):
        self.api_tree = api_tree

    def make_all(self):
        for request_node in self.api_tree.request_nodes:
            request_node.evaluate_request()
            try:
                response = self.make_request(request_node)
            except Exception as e:
                error_message = f"Error to make request `{request_node.id}`. {str(e)}"
                logger.error(error_message)
                continue

            self.api_tree.responses[request_node.id] = response
            self.api_tree.save_custom_vars(request_node.spec)

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
            allow_redirects=False,
        )

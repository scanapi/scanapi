#!/usr/bin/env python3
import click
import logging
import requests
import yaml

from scanapi.errors import HTTPMethodNotAllowedError
from scanapi.variable_parser import save_response

logger = logging.getLogger(__name__)


class RequestsMaker:
    ALLOWED_HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")

    def __init__(self, requests):
        self.requests = requests
        self.responses = []

    def make_all(self):
        for request in self.requests:
            request.evaluate_request()
            try:
                response = self.make_request(request)
            except Exception as e:
                error_message = f"Error to make request `{request.id}`. {str(e)}"
                logger.error(error_message)
                continue
            save_response(request.id, response)
            self.responses.append(response)

            request.save_custom_vars(dynamic_chain=True)

        return self.responses

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

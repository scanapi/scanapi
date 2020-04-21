import logging
import requests

from scanapi.errors import HTTPMethodNotAllowedError
from scanapi.evaluators import SpecEvaluator
from scanapi.tree.tree_keys import (
    BODY_KEY,
    HEADERS_KEY,
    METHOD_KEY,
    NAME_KEY,
    PARAMS,
    PATH_KEY,
    VARS_KEY,
)
from scanapi.utils import join_urls, hide_sensitive_info, validate_keys

logger = logging.getLogger(__name__)


class RequestNode:
    SCOPE = "request"
    ALLOWED_KEYS = (
        BODY_KEY,
        HEADERS_KEY,
        METHOD_KEY,
        NAME_KEY,
        PARAMS,
        PATH_KEY,
        VARS_KEY,
    )
    ALLOWED_HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")

    def __init__(self, spec, endpoint):
        self.spec = spec
        self.endpoint = endpoint
        self._validate()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.full_url_path}>"

    def __getitem__(self, item):
        return self.spec[item]

    @property
    def http_method(self):
        method = self.spec.get("method", "get").upper()
        if method not in self.ALLOWED_HTTP_METHODS:
            raise HTTPMethodNotAllowedError(method, self.ALLOWED_HTTP_METHODS)

        return method

    @property
    def name(self):
        return self["name"]

    @property
    def full_url_path(self):
        base_path = self.endpoint.path
        path = self.spec.get("path", "")
        full_url = join_urls(base_path, path)

        return self.endpoint.vars.evaluate(full_url)

    @property
    def headers(self):
        endpoint_headers = self.endpoint.headers
        headers = self.spec.get("headers", {})

        return self.endpoint.vars.evaluate({**endpoint_headers, **headers})

    @property
    def params(self):
        endpoint_params = self.endpoint.params
        params = self.spec.get("params", {})

        return self.endpoint.vars.evaluate({**endpoint_params, **params})

    @property
    def body(self):
        body = self.spec.get("body", {})

        return self.endpoint.vars.evaluate(body)

    def run(self):
        method = self.http_method
        url = self.full_url_path
        logger.info("Making request %s %s", method, url)

        response = requests.request(
            method,
            url,
            headers=self.headers,
            params=self.params,
            json=self.body,
            allow_redirects=False,
        )

        self.endpoint.vars.update(
            self.spec.get("vars", {}), extras={"response": response}, preevaluate=True
        )

        hide_sensitive_info(response)
        return response

    def _validate(self):
        validate_keys(self.spec.keys(), self.ALLOWED_KEYS, self.SCOPE)

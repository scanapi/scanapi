import requests

from scanapi.refactor.evaluators import SpecEvaluator
from scanapi.refactor.utils import join_urls, hide_sensitive_info


class RequestNode:
    def __init__(self, spec, endpoint):
        self.spec = spec
        self.endpoint = endpoint

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.full_url_path}>"

    def __getitem__(self, item):
        return self.spec[item]

    @property
    def http_method(self):
        return self.spec.get("method", "get")

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
        response = requests.request(
            self.http_method,
            self.full_url_path,
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

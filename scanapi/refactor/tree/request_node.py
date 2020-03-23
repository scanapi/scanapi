import requests

from scanapi.refactor.evaluators import SpecEvaluator, StringEvaluator
from scanapi.refactor.utils import join_urls


class RequestNode:
    def __init__(self, spec, endpoint):
        self.spec = spec
        self.endpoint = endpoint

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.full_url_path}>"

    def __getitem__(self, item):
        return self.spec[item]

    @property
    def name(self):
        return self["name"]

    @property
    def full_url_path(self):
        base_path = self.endpoint.path
        path = self.spec.get("path", "")
        full_url = join_urls(base_path, path)

        return StringEvaluator.evaluate(full_url)

    @property
    def headers(self):
        endpoint_headers = self.endpoint.headers
        headers = self.spec.get("headers", {})

        return SpecEvaluator.evaluate({**endpoint_headers, **headers})

    @property
    def method(self):
        return self.spec.get("method", "get")

    def run(self):
        response = requests.request(
            self.method, self.full_url_path, headers=self.headers, allow_redirects=False
        )
        # TODO: hide headers
        return response

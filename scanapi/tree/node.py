from itertools import chain

import requests

from scanapi.errors import BadConfigurationError
from scanapi.tree.endpoint_node import join_urls

import os
import re


class EndpointNode:
    def __init__(self, spec, parent=None):
        self.spec = spec
        self.parent = parent
        self.child_nodes = []
        self.__build()

    def __build(self):
        self.child_nodes = [
            EndpointNode(spec, parent=self) for spec in self.spec.get("endpoints", [])
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.namespace}>"

    @property
    def namespace(self):
        return self.spec.get("namespace", "root")

    def get_requests(self):
        return chain(
            (RequestNode(spec, self) for spec in self.spec.get("requests", [])),
            *(child.get_requests() for child in self.child_nodes),
        )

    def run(self):
        for request in self.get_requests():
            yield request.run()

    @property
    def path(self):
        path = self.spec.get("path", "").strip()
        if self.parent and self.parent.path:
            return join_urls(self.parent.path, path)

        return StringEvaluator().evaluate(path)

    @property
    def headers(self):
        headers = self.spec.get("headers", {})

        if self.parent and self.parent.headers:
            return {**self.parent.headers, **headers}

        return headers


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
        if path:
            return join_urls(base_path, path)
        return base_path

    @property
    def headers(self):
        endpoint_headers = self.endpoint.headers
        headers = self.spec.get("headers", {})

        return {**endpoint_headers, **headers}

    @property
    def method(self):
        return self.spec.get("method", "get")

    def run(self):
        response = requests.request(
            self.method, self.full_url_path, headers=self.headers, allow_redirects=False
        )
        # TODO: hide headers
        return response


class StringEvaluator:
    variable_pattern = re.compile(
        r"(?P<something_before>\w*)(?P<start>\${)(?P<variable>\w*)(?P<end>})(?P<something_after>\w*)"
    )  # ${<variable>}

    def evaluate(self, sequence):
        try:
            return self.evaluate_env_var(sequence)
        except BadConfigurationError as e:
            logger.error(e)
            sys.exit()

    def evaluate_env_var(self, sequence):
        matches = self.variable_pattern.finditer(sequence)

        if not matches:
            return sequence

        for match in matches:
            variable_name = match.group("variable")

            if any(letter.islower() for letter in variable_name):
                continue

            try:
                variable_value = os.environ[variable_name]
            except KeyError as e:
                raise BadConfigurationError(e)

            sequence = self.replace_var_with_value(
                sequence, match.group(), variable_value
            )

        return sequence

    def replace_var_with_value(self, sequence, variable, variable_value):
        variable = re.escape(variable)
        return re.sub(variable, variable_value, sequence)

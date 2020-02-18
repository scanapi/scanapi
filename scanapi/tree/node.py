from itertools import chain

import requests

from scanapi.tree.endpoint_node import join_urls


class EndpointNode:
    def __init__(self, spec, parent=None):
        self.spec = spec
        self.parent = parent
        self.child_nodes = []
        self.__build()

    def __build(self):
        self.child_nodes = [
            EndpointNode(spec, parent=self)
            for spec in self.spec.get("endpoints", [])
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.namespace}>"

    @property
    def namespace(self):
        return self.spec.get("namespace", "root")

    def get_requests(self):
        return chain(
            (
                RequestNode(spec, self)
                for spec in self.spec.get("requests", [])
            ),
            *(
                child.get_requests()
                for child in self.child_nodes
            )
        )

    @property
    def path(self):
        path = self.spec.get("path", "").strip()
        if self.parent and self.parent.path:
            return join_urls(self.parent.path, path)
        return path


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
    def method(self):
        return self.spec.get("method", "get")

    def run(self):
        return requests.request(
            self.method,
            self.full_url_path,
            allow_redirects=False,
        )

from itertools import chain


from scanapi.refactor.evaluators import StringEvaluator
from scanapi.refactor.tree.request_node import RequestNode
from scanapi.refactor.utils import join_urls


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
        url = join_urls(self.parent.path, path) if self.parent else path

        return StringEvaluator.evaluate(url)

    @property
    def headers(self):
        headers = self.spec.get("headers", {})

        if self.parent and self.parent.headers:
            return {**self.parent.headers, **headers}

        return headers

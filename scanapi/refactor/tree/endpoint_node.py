from itertools import chain


from scanapi.refactor.evaluators import SpecEvaluator
from scanapi.refactor.tree.request_node import RequestNode
from scanapi.refactor.utils import join_urls


class EndpointNode:
    def __init__(self, spec, parent=None):
        self.spec = spec
        self.parent = parent
        self.child_nodes = []
        self.__build()
        self.vars = SpecEvaluator(self, spec.get("vars", {}))

    def __build(self):
        self.child_nodes = [
            EndpointNode(spec, parent=self) for spec in self.spec.get("endpoints", [])
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @property
    def name(self):
        return self.spec.get("name", "root")

    @property
    def path(self):
        path = self.spec.get("path", "").strip()
        url = join_urls(self.parent.path, path) if self.parent else path

        return self.vars.evaluate(url)

    @property
    def headers(self):
        return self._get_specs("headers")

    @property
    def params(self):
        return self._get_specs("params")

    def run(self):
        for request in self._get_requests():
            yield request.run()

    def _get_specs(self, field_name):
        values = self.spec.get(field_name, {})
        parent_values = getattr(self.parent, field_name, None)

        if parent_values:
            return {**parent_values, **values}

        return values

    def _get_requests(self):
        return chain(
            (RequestNode(spec, self) for spec in self.spec.get("requests", [])),
            *(child._get_requests() for child in self.child_nodes),
        )

from scanapi.errors import ROOT_SCOPE
from scanapi.tree.api_node import APINode
from scanapi.tree.tree_keys import ROOT_NODE_KEYS


class RootNode(APINode):
    def __init__(self, api_tree):
        super().__init__(api_tree, api_tree.spec)

        self.url = self.define_url()
        self.headers = self.define_headers()
        self.params = self.define_params()
        self.namespace = ""

    def define_url(self):
        return self.spec_evaluator.evaluate(self.spec["base_url"])

    def define_headers(self):
        if "headers" not in self.spec:
            return

        return self.spec_evaluator.evaluate(self.spec["headers"])

    def define_params(self):
        if "params" not in self.spec:
            return

        return self.spec_evaluator.evaluate(self.spec["params"])

    def validate(self):
        APINode.validate_keys(self.spec.keys(), ROOT_NODE_KEYS, ROOT_SCOPE)

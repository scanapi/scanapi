from scanapi.tree.api_node import APINode
from scanapi.variable_parser import EvaluationType, evaluate


class RootNode(APINode):
    def __init__(self, node_spec):
        self.spec = node_spec
        self.url = self.define_url()
        self.headers = self.define_headers()
        self.params = self.define_params()
        self.namespace = ""
        self.custom_vars = {}

    def define_url(self):
        return evaluate(EvaluationType.ENV_VAR, self.spec["base_url"])

    def define_headers(self):
        if "headers" not in self.spec:
            return {}

        return evaluate(EvaluationType.ENV_VAR, self.spec["headers"])

    def define_params(self):
        if "params" not in self.spec:
            return {}

        return evaluate(EvaluationType.ENV_VAR, self.spec["params"])

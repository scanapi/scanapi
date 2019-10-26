from scanapi.tree.api_node import APINode
from scanapi.variable_parser import EvaluationType, evaluate


class EndpointNode(APINode):
    def __init__(self, node_spec, parent=None):
        self.spec = node_spec
        self.parent = parent
        self.url = self.define_url()
        self.headers = self.define_headers()
        self.params = self.define_params()
        self.namespace = self.define_namespace()
        self.custom_vars = {}

    def define_url(self):
        parent_url = self.parent.url

        if "path" not in self.spec:
            return parent_url

        populated_node_path = str(evaluate(EvaluationType.ENV_VAR, self.spec["path"]))
        return "/".join(s.strip("/") for s in [parent_url, populated_node_path])

    def define_headers(self):
        parent_headers = self.parent.headers

        if "headers" not in self.spec:
            return parent_headers

        return {
            **parent_headers,
            **evaluate(EvaluationType.ENV_VAR, self.spec["headers"]),
        }

    def define_params(self):
        parent_params = self.parent.params

        if "params" not in self.spec:
            return parent_params

        return {
            **parent_params,
            **evaluate(EvaluationType.ENV_VAR, self.spec["params"]),
        }

    def define_namespace(self):
        parent_namespace = self.parent.namespace

        if "namespace" not in self.spec:
            return parent_namespace

        populated_node_namespace = evaluate(
            EvaluationType.ENV_VAR, self.spec["namespace"]
        )

        return "_".join(filter(None, [parent_namespace, populated_node_namespace]))

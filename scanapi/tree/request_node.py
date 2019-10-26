from scanapi.errors import REQUEST_SCOPE
from scanapi.tree.api_node import APINode
from scanapi.tree.endpoint_node import EndpointNode
from scanapi.tree.tree_keys import REQUEST_NODE_KEYS
from scanapi.variable_parser import EvaluationType, evaluate


class RequestNode(EndpointNode):
    def __init__(self, node_spec, parent):
        super().__init__(node_spec, parent)

        self.method = self.spec["method"]
        self.body = self.define_body()
        self.id = self.define_id()

        self.save_custom_vars()

    def evaluate_request(self):
        self.url = evaluate(EvaluationType.CUSTOM_VAR, self.url, self)
        self.url = evaluate(EvaluationType.PYTHON_CODE, self.url)
        self.headers = evaluate(EvaluationType.CUSTOM_VAR, self.headers, self)
        self.headers = evaluate(EvaluationType.PYTHON_CODE, self.headers)
        self.params = evaluate(EvaluationType.CUSTOM_VAR, self.params, self)
        self.params = evaluate(EvaluationType.PYTHON_CODE, self.params)
        self.body = evaluate(EvaluationType.CUSTOM_VAR, self.body, self)
        self.body = evaluate(EvaluationType.PYTHON_CODE, self.body)

    def define_body(self):
        if "body" not in self.spec:
            return {}

        return evaluate(EvaluationType.ENV_VAR, self.spec["body"])

    def define_id(self):
        if not self.namespace:
            return self.spec["name"]

        return "{}_{}".format(self.namespace, self.spec["name"])

    def save_custom_vars(self, dynamic_chain=False):
        parent_vars = self.parent.custom_vars
        key = self.custom_vars_key(dynamic_chain)

        if key not in self.spec:
            return parent_vars

        node_vars = {}

        for var_name, var_value in self.spec[key].items():
            node_vars[var_name] = evaluate(EvaluationType.ENV_VAR, var_value)

        self.parent.custom_vars = {**parent_vars, **node_vars}

    def custom_vars_key(self, dynamic_chain):
        if dynamic_chain:
            return "dcvars"

        return "vars"

    def validate(self):
        APINode.validate_keys(self.spec.keys(), REQUEST_NODE_KEYS, REQUEST_SCOPE)

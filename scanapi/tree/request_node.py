from scanapi.errors import REQUEST_SCOPE
from scanapi.tree.api_node import APINode
from scanapi.tree.endpoint_node import EndpointNode
from scanapi.tree.tree_keys import REQUEST_NODE_KEYS
from scanapi.variable_parser import evaluate


class RequestNode(EndpointNode):
    def __init__(self, api_tree, node_spec, parent):
        super().__init__(api_tree, node_spec, parent)

        self.method = self.spec["method"]
        self.body = self.define_body()
        self.id = self.define_id()

        self.api_tree.save_custom_vars(self.spec)

    def evaluate_request(self):
        self.url = evaluate(self.api_tree, self.url)
        self.headers = evaluate(self.api_tree, self.headers)
        self.params = evaluate(self.api_tree, self.params)
        self.body = evaluate(self.api_tree, self.body)

    def define_body(self):
        if "body" not in self.spec:
            return {}

        return evaluate(self.api_tree, self.spec["body"])

    def define_id(self):
        if not self.namespace:
            return self.spec["name"]

        return f"{self.namespace}_{self.spec['name']}"

    def validate(self):
        APINode.validate_keys(self.spec.keys(), REQUEST_NODE_KEYS, REQUEST_SCOPE)

from scanapi.errors import ENDPOINT_SCOPE
from scanapi.tree.api_node import APINode
from scanapi.tree.tree_keys import ENDPOINT_NODE_KEYS


class EndpointNode(APINode):
    def __init__(self, api_tree, node_spec, parent):
        super().__init__(api_tree, node_spec)

        self.parent = parent
        self.url = self.define_url()
        self.headers = self.define_headers()
        self.params = self.define_params()
        self.namespace = self.define_namespace()

    def define_url(self):
        parent_url = self.parent.url

        if "path" not in self.spec:
            return parent_url

        populated_node_path = str(self.spec_evaluator.evaluate(self.spec["path"]))

        return join_urls(parent_url, populated_node_path)

    def define_headers(self):
        parent_headers = self.parent.headers

        if "headers" not in self.spec:
            return parent_headers

        return {**parent_headers, **self.spec_evaluator.evaluate(self.spec["headers"])}

    def define_params(self):
        parent_params = self.parent.params

        if "params" not in self.spec:
            return parent_params

        return {**parent_params, **self.spec_evaluator.evaluate(self.spec["params"])}

    def define_namespace(self):
        parent_namespace = self.parent.namespace

        if "namespace" not in self.spec:
            return parent_namespace

        populated_node_namespace = self.spec_evaluator.evaluate(self.spec["namespace"])

        return "_".join(filter(None, [parent_namespace, populated_node_namespace]))

    def validate(self):
        APINode.validate_keys(self.spec.keys(), ENDPOINT_NODE_KEYS, ENDPOINT_SCOPE)


def join_urls(first_url, second_url):
    first_url = first_url.strip("/")
    second_url = second_url.lstrip("/")

    return "/".join([first_url, second_url])

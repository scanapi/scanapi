from scanapi.variable_parser import populate_dict, populate_str


class APINode:
    def __init__(self, node_spec, parent=None):
        self.spec = node_spec
        self.parent = parent
        self.url = self.define_url()
        self.headers = self.define_headers()
        self.params = self.define_params()
        self.namespace = self.define_namespace()
        self.custom_vars = {}

    def define_url(self):
        parent_url = (
            self.parent.url
            if self.parent
            else populate_str(self.spec["base_url"], self)
        )

        if "path" not in self.spec:
            return parent_url

        populated_node_path = populate_str(self.spec["path"], self)
        return "/".join(s.strip("/") for s in [parent_url, populated_node_path])

    def define_headers(self):
        parent_headers = self.parent.headers if self.parent else {}

        if "headers" not in self.spec:
            return parent_headers

        return {**parent_headers, **populate_dict(self.spec["headers"], self)}

    def define_params(self):
        parent_params = self.parent.params if self.parent else {}

        if "params" not in self.spec:
            return parent_params

        return {**parent_params, **populate_dict(self.spec["params"], self)}

    def define_namespace(self):
        parent_namespace = self.parent.namespace if self.parent else ""

        if "namespace" not in self.spec:
            return parent_namespace

        populated_node_namespace = populate_str(self.spec["namespace"], self)

        return "_".join(filter(None, [parent_namespace, populated_node_namespace]))


class RequestNode(APINode):
    def __init__(self, node_spec, parent):
        if not parent:
            print("Request must have an endpoint parent")

        self.spec = node_spec
        self.parent = parent
        self.url = self.define_url()
        self.headers = self.define_headers()
        self.params = self.define_params()
        self.namespace = self.define_namespace()
        self.body = self.define_body()

    def define_body(self):
        if "body" not in self.spec:
            return {}

        return populate_dict(self.spec["body"], self)

    def save_custom_vars(self):
        parent_vars = self.parent.custom_vars

        if "vars" not in self.spec:
            return parent_vars

        node_vars = {}

        for var_name, var_value in self.spec["vars"].items():
            node_vars[var_name] = populate_str(var_value, self)

        self.parent.custom_vars = {**parent_vars, **node_vars}

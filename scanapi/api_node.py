from scanapi.variable_parser import EvaluationType, evaluate


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
        if not self.parent:
            parent_url = evaluate(EvaluationType.ENV_VAR, self.spec["base_url"])
        else:
            parent_url = self.parent.url

        if "path" not in self.spec:
            return parent_url

        populated_node_path = evaluate(EvaluationType.ENV_VAR, self.spec["path"])
        return "/".join(s.strip("/") for s in [parent_url, populated_node_path])

    def define_headers(self):
        parent_headers = self.parent.headers if self.parent else {}

        if "headers" not in self.spec:
            return parent_headers

        return {
            **parent_headers,
            **evaluate(EvaluationType.ENV_VAR, self.spec["headers"]),
        }

    def define_params(self):
        parent_params = self.parent.params if self.parent else {}

        if "params" not in self.spec:
            return parent_params

        return {
            **parent_params,
            **evaluate(EvaluationType.ENV_VAR, self.spec["params"]),
        }

    def define_namespace(self):
        parent_namespace = self.parent.namespace if self.parent else ""

        if "namespace" not in self.spec:
            return parent_namespace

        populated_node_namespace = evaluate(
            EvaluationType.ENV_VAR, self.spec["namespace"]
        )

        return "_".join(filter(None, [parent_namespace, populated_node_namespace]))


class RequestNode(APINode):
    def __init__(self, node_spec, parent):
        super().__init__(node_spec, parent)
        self.method = self.spec["method"]
        self.body = self.define_body()
        if self.namespace:
            self.id = "{}_{}".format(self.namespace, self.spec["name"])
        else:
            self.id = self.spec["name"]

    def evaluate_request(self):
        request_path = self.url.rsplit("/", 1)[-1]
        evaluated_path = evaluate(EvaluationType.CUSTOM_VAR, request_path, self)
        evaluated_path = evaluate(EvaluationType.PYTHON_CODE, evaluated_path)
        self.url = self.url.replace(request_path, evaluated_path)

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

    def save_custom_vars(self):
        parent_vars = self.parent.custom_vars

        if "vars" not in self.spec:
            return parent_vars

        node_vars = {}

        for var_name, var_value in self.spec["vars"].items():
            node_vars[var_name] = evaluate(EvaluationType.ENV_VAR, var_value)

        self.parent.custom_vars = {**parent_vars, **node_vars}

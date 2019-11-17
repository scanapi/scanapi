import logging

from scanapi.tree.api_node import APINode
from scanapi.tree.endpoint_node import EndpointNode
from scanapi.tree.request_node import RequestNode
from scanapi.tree.root_node import RootNode
from scanapi.errors import APIKeyMissingError
from scanapi.evaluators.spec_evaluator import SpecEvaluator

logger = logging.getLogger(__name__)


class APITree:
    def __init__(self, api_spec):
        if "api" not in api_spec:
            raise APIKeyMissingError

        self.spec = api_spec["api"]
        self.request_nodes = []  # tree's leaves
        self.responses = {}
        self.custom_vars = {}
        self.spec_evaluator = SpecEvaluator(self)
        self.root = RootNode(self)

        self.build()

    def build(self):
        logger.info("Building requests")

        # Builds the root requests
        if "requests" in self.spec:
            self.build_requests(self.root)

        if not "endpoints" in self.spec:
            return

        self.build_endpoints(self.root)

    def build_endpoints(self, parent):
        for endpoint_spec in parent.spec["endpoints"]:
            endpoint = EndpointNode(self, endpoint_spec, parent)

            if "requests" in endpoint.spec:
                self.build_requests(endpoint)

            if "endpoints" in endpoint.spec:
                self.build_endpoints(endpoint)

    def build_requests(self, endpoint):
        for request_spec in endpoint.spec["requests"]:
            self.request_nodes.append(RequestNode(self, request_spec, endpoint))

    def save_custom_vars(self, node_spec):
        if "vars" not in node_spec:
            return

        for var_name, var_value in node_spec["vars"].items():
            self.custom_vars[var_name] = self.spec_evaluator.evaluate(var_value)

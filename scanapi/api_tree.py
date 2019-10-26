import logging

from scanapi.api_node import APINode, RequestNode
from scanapi.errors import APIKeyMissingError

logger = logging.getLogger(__name__)


class APITree:
    def __init__(self, api_spec):
        if "api" not in api_spec:
            raise APIKeyMissingError

        self.spec = api_spec["api"]
        self.root = APINode(self.spec)
        self.leaves = []

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
            endpoint = APINode(endpoint_spec, parent)

            if "requests" in endpoint.spec:
                self.build_requests(endpoint)

            if "endpoints" in endpoint.spec:
                self.build_endpoints(endpoint)

    def build_requests(self, endpoint):
        for request_spec in endpoint.spec["requests"]:
            self.leaves.append(RequestNode(request_spec, endpoint))

    @property
    def requests(self):
        return self.leaves

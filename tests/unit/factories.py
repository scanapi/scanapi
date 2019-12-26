import factory

from scanapi.reporter import Reporter
from scanapi.requests_maker import RequestsMaker
from scanapi.tree.api_node import APINode
from scanapi.tree.api_tree import APITree
from scanapi.tree.endpoint_node import EndpointNode
from scanapi.yaml_loader import load_yaml


WITH_ENDPOINTS_MINIMAL_SPEC = load_yaml(
    "tests/data/specs/with_endpoints/minimal_get.yaml"
)
WITH_ENDPOINTS_WITH_ROOT_REQUESTS = load_yaml(
    "tests/data/specs/with_endpoints/get_with_root_requests.yaml"
)
WITH_ENDPOINTS_GET_WITH_HEADER_BODY_PARAMS = load_yaml(
    "tests/data/specs/with_endpoints/get_with_header_body_params.yaml"
)
WITHOUT_ENDPOINTS_MINIMAL_SPEC = load_yaml(
    "tests/data/specs/without_endpoints/minimal_get.yaml"
)
METHOD_NOT_ALLOWED_SPEC = load_yaml("tests/data/specs/invalid/method_not_allowed.yaml")


class APITreeFactory(factory.Factory):
    class Meta:
        model = APITree

    api_spec = WITHOUT_ENDPOINTS_MINIMAL_SPEC

    class Params:
        with_endpoints_minimal = factory.Trait(api_spec=WITH_ENDPOINTS_MINIMAL_SPEC)
        with_endpoints_with_root_requests = factory.Trait(
            api_spec=WITH_ENDPOINTS_WITH_ROOT_REQUESTS
        )
        with_endpoints_get_with_header_body_params = factory.Trait(
            api_spec=WITH_ENDPOINTS_GET_WITH_HEADER_BODY_PARAMS
        )
        without_endpoints_minimal = factory.Trait(
            api_spec=WITHOUT_ENDPOINTS_MINIMAL_SPEC
        )
        method_not_allowed = factory.Trait(api_spec=METHOD_NOT_ALLOWED_SPEC)


class EndpointNodeFactory(factory.Factory):
    class Meta:
        model = EndpointNode


class RequestsMakerFactory(factory.Factory):
    class Meta:
        model = RequestsMaker

    api_tree = factory.SubFactory(APITreeFactory)


class ReporterFactory(factory.Factory):
    class Meta:
        model = Reporter

    output_path = "reports/"
    reporter = "markdown"
    template = "templates/my_template"

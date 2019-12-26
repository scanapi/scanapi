import pytest

from scanapi.tree.endpoint_node import join_urls
from tests.unit.factories import APITreeFactory


class TestEndpointNode:
    @pytest.fixture
    def tree(self):
        return APITreeFactory(with_endpoints_minimal=True)

    @pytest.fixture
    def root_node(self, tree):
        return tree.root

    @pytest.fixture
    def endpoint_node(self, tree):
        return tree.request_nodes[0].parent

    class TestDefineUrl:
        pass

    class TestDefineHeaders:
        class TestWhenParentHasNoHeaders:
            def test_return_none(self, root_node, endpoint_node):
                root_node.headers = None
                assert endpoint_node.define_headers() is None

        class TestWhenParentHasHeadersAndEndpointNodeDoesnt:
            def test_return_parents_headers(self, root_node, endpoint_node):
                parent_headers = {"parent_headers": "testing"}
                root_node.headers = parent_headers
                endpoint_node.headers = None
                assert endpoint_node.define_headers() == parent_headers

        class TestWhenParentAndEndpointNodeHaveHeaders:
            def test_return_merged_headers(self, root_node, endpoint_node):
                root_node.headers = {"parent_headers": "testing"}
                endpoint_node.spec["headers"] = {"endpoint_node_headers": "testing"}

                assert endpoint_node.define_headers() == {
                    "parent_headers": "testing",
                    "endpoint_node_headers": "testing",
                }

    class TestDefineParams:
        class TestWhenParentHasNoParams:
            def test_return_none(self, root_node, endpoint_node):
                root_node.params = None
                assert endpoint_node.define_params() is None

        class TestWhenParentHasParamsAndEndpointNodeDoesnt:
            def test_return_parents_params(self, root_node, endpoint_node):
                parent_params = {"parent_params": "testing"}
                root_node.params = parent_params
                endpoint_node.params = None
                assert endpoint_node.define_params() == parent_params

        class TestWhenParentAndEndpointNodeHaveHeaders:
            def test_return_merged_params(self, root_node, endpoint_node):
                root_node.params = {"parent_params": "testing"}
                endpoint_node.spec["params"] = {"endpoint_node_params": "testing"}

                assert endpoint_node.define_params() == {
                    "parent_params": "testing",
                    "endpoint_node_params": "testing",
                }

    class TestDefineNamespace:
        pass

    class TestValidate:
        pass


class TestJoinUrls:
    test_data = [
        (
            "http://demo.scanapi.dev/api/",
            "health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api/",
            "/health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api/",
            "/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
        ("http://demo.scanapi.dev/api", "health", "http://demo.scanapi.dev/api/health"),
        (
            "http://demo.scanapi.dev/api",
            "/health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api",
            "/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
    ]

    @pytest.mark.parametrize("url_1, url_2, expected", test_data)
    def test_build_url_properly(self, url_1, url_2, expected):
        assert join_urls(url_1, url_2) == expected

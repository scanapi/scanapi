import pytest

from tests.unit.factories import (
    APITreeFactory,
    WITHOUT_ENDPOINTS_MINIMAL_SPEC,
    WITH_ENDPOINTS_MINIMAL_SPEC,
    WITH_ENDPOINTS_WITH_ROOT_REQUESTS,
)


class TestAPITree:
    @pytest.fixture
    def mock_build_endpoints(self, mocker):
        return mocker.patch("scanapi.tree.api_tree.APITree.build_endpoints")

    @pytest.fixture
    def mock_build_requests(self, mocker):
        return mocker.patch("scanapi.tree.api_tree.APITree.build_requests")

    class TestWhenSpecHasEndpointsAndNoRootRequests:
        def test_build_endpoints_should_be_called(
            self, mock_build_endpoints, mock_build_requests
        ):
            APITreeFactory(api_spec=WITH_ENDPOINTS_MINIMAL_SPEC)

            assert mock_build_endpoints.called_once
            assert not mock_build_requests.called

        def test_should_build_requests(self):
            api_tree = APITreeFactory(with_endpoints_minimal=True)
            request = api_tree.request_nodes[0]

            assert len(api_tree.request_nodes) == 1
            assert request.spec == {"name": "list_all_posts", "method": "get"}
            assert request.id == "posts_list_all_posts"
            assert request.url == "https://jsonplaceholder.typicode.com/posts"
            assert request.method == "get"
            assert request.body is None
            assert request.headers is None

    class TestWhenSpecHasRootRequestsAndDoesNotHaveEndpoints:
        def test_build_request_should_be_called(
            self, mock_build_endpoints, mock_build_requests
        ):
            APITreeFactory(api_spec=WITHOUT_ENDPOINTS_MINIMAL_SPEC)
            assert mock_build_requests.called_once

        def test_should_build_requests(self):
            api_tree = APITreeFactory(without_endpoints_minimal=True)
            request = api_tree.request_nodes[0]

            assert request.spec == {
                "name": "list_all_posts",
                "path": "/posts",
                "method": "get",
            }
            assert len(api_tree.request_nodes) == 1
            assert request.id == "list_all_posts"
            assert request.url == "https://jsonplaceholder.typicode.com/posts"
            assert request.method == "get"
            assert request.body is None
            assert request.headers is None

    class TestWhenSpecHasRootRequestAndEndpoints:
        def test_build_request_should_be_called(
            self, mock_build_endpoints, mock_build_requests
        ):
            APITreeFactory(api_spec=WITH_ENDPOINTS_WITH_ROOT_REQUESTS)

            assert mock_build_requests.called_once
            assert mock_build_requests.called_once

        def test_should_build_requests(self):
            api_tree = APITreeFactory(with_endpoints_with_root_requests=True)
            root_request = api_tree.request_nodes[0]

            assert len(api_tree.request_nodes) == 2
            assert root_request.spec == {
                "name": "docs",
                "method": "get",
                "path": "docs",
            }
            assert root_request.id == "docs"
            assert root_request.url == "https://jsonplaceholder.typicode.com/docs"
            assert root_request.method == "get"
            assert root_request.body is None
            assert root_request.headers is None

            endpoint_request = api_tree.request_nodes[1]
            assert endpoint_request.spec == {"name": "list_all_posts", "method": "get"}
            assert endpoint_request.id == "posts_list_all_posts"
            assert endpoint_request.url == "https://jsonplaceholder.typicode.com/posts"
            assert endpoint_request.method == "get"
            assert endpoint_request.body is None
            assert endpoint_request.headers is None

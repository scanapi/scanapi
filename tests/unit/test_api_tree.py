import pytest

from scanapi.api_tree import APITree
from scanapi.yaml_loader import load_yaml


class TestAPITree:
    class TestBuild:
        @pytest.fixture
        def mock_build_endpoints(self, mocker):
            return mocker.patch("scanapi.api_tree.APITree.build_endpoints")

        @pytest.fixture
        def mock_build_requests(self, mocker):
            return mocker.patch("scanapi.api_tree.APITree.build_requests")

        class TestWhenSpecHasEndpoints:
            @pytest.fixture
            def api_spec(self):
                return load_yaml("tests/data/specs/with_endpoints/minimal_get.yaml")

            def test_should_build_requests(self, api_spec):
                api_tree = APITree(api_spec)
                request = api_tree.requests[0]

                assert len(api_tree.requests) == 1
                assert request.spec == {"name": "list_all_posts", "method": "get"}
                assert request.id == "posts_list_all_posts"
                assert request.url == "https://jsonplaceholder.typicode.com/posts"
                assert request.custom_vars == {}
                assert request.method == "get"
                assert request.body == {}
                assert request.headers == {}

            def test_build_endpoints_should_be_called(
                self, api_spec, mock_build_endpoints, mock_build_requests
            ):
                APITree(api_spec)

                assert mock_build_endpoints.called_once
                assert not mock_build_requests.called

        class TestWhenSpecDoesNotHaveEndpoints:
            @pytest.fixture
            def api_spec(self):
                return load_yaml("tests/data/specs/without_endpoints/minimal_get.yaml")

            def test_should_build_requests(self, api_spec):
                api_tree = APITree(api_spec)
                request = api_tree.requests[0]

                assert len(api_tree.requests) == 1
                assert request.spec == {
                    "name": "list_all_posts",
                    "path": "/posts",
                    "method": "get",
                }
                assert request.id == "list_all_posts"
                assert request.url == "https://jsonplaceholder.typicode.com/posts"
                assert request.custom_vars == {}
                assert request.method == "get"
                assert request.body == {}
                assert request.headers == {}

            def test_build_request_should_be_called(
                self, api_spec, mock_build_endpoints, mock_build_requests
            ):
                APITree(api_spec)
                assert mock_build_requests.called_once

        class TestWhenSpecHasRootRequestAndEndpoints:
            @pytest.fixture
            def api_spec(self):
                return load_yaml(
                    "tests/data/specs/with_endpoints/get_with_root_requests.yaml"
                )

            def test_should_build_requests(self, api_spec):
                api_tree = APITree(api_spec)
                assert len(api_tree.requests) == 2

                root_request = api_tree.requests[0]
                assert root_request.spec == {
                    "name": "docs",
                    "method": "get",
                    "path": "docs",
                }
                assert root_request.id == "docs"
                assert root_request.url == "https://jsonplaceholder.typicode.com/docs"
                assert root_request.custom_vars == {}
                assert root_request.method == "get"
                assert root_request.body == {}
                assert root_request.headers == {}

                endpoint_request = api_tree.requests[1]
                assert endpoint_request.spec == {
                    "name": "list_all_posts",
                    "method": "get",
                }
                assert endpoint_request.id == "posts_list_all_posts"
                assert (
                    endpoint_request.url == "https://jsonplaceholder.typicode.com/posts"
                )
                assert endpoint_request.custom_vars == {}
                assert endpoint_request.method == "get"
                assert endpoint_request.body == {}
                assert endpoint_request.headers == {}

            def test_build_request_should_be_called(
                self, api_spec, mock_build_endpoints, mock_build_requests
            ):
                APITree(api_spec)

                assert mock_build_requests.called_once
                assert mock_build_requests.called_once

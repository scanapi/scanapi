import pytest

from scanapi.refactor.tree import EndpointNode, RequestNode


class TestRequestNode:
    class TestFullPathUrl:
        @pytest.fixture
        def mock_evaluate(self, mocker):
            mock_func = mocker.patch(
                "scanapi.refactor.tree.request_node.StringEvaluator.evaluate"
            )
            mock_func.return_value = ""

            return mock_func

        def test_request_with_no_path(self):
            base_path = "http://foo.com/"
            request = RequestNode({}, endpoint=EndpointNode({"path": base_path}))
            assert request.full_url_path == base_path

        def test_when_endpoint_has_no_url(self):
            path = "http://foo.com"
            request = RequestNode({"path": path}, endpoint=EndpointNode({}))
            assert request.full_url_path == path

        def test_when_endpoint_has_url(self):
            endpoint_path = "http://foo.com/api"
            endpoint = EndpointNode({"path": endpoint_path})
            request = RequestNode({"path": "/foo"}, endpoint=endpoint)
            assert request.full_url_path == f"http://foo.com/api/foo"

        def test_with_trailing_slashes(self):
            endpoint = EndpointNode({"path": "http://foo.com/"})
            request = RequestNode({"path": "/foo/"}, endpoint=endpoint)
            assert request.full_url_path == "http://foo.com/foo/"

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode({"path": "http://foo.com/"})
            request = RequestNode({"path": "/foo/"}, endpoint=endpoint)
            request.full_url_path
            calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

            mock_evaluate.assert_has_calls(calls)

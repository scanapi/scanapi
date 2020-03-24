import pytest

from scanapi.refactor.tree import EndpointNode


class TestEndpointNode:
    @pytest.fixture
    def empty_node(self):
        return EndpointNode({})

    class TestInit:
        def test_should_create_children(self):
            endpoints = [{}, {}]
            node = EndpointNode({"endpoints": endpoints})
            assert len(node.child_nodes) == len(endpoints)

    class TestName:
        def test_when_node_is_empty(self, empty_node):
            assert empty_node.name == "root"

    class TestPath:
        @pytest.fixture
        def mock_evaluate(self, mocker):
            mock_func = mocker.patch(
                "scanapi.refactor.tree.endpoint_node.StringEvaluator.evaluate"
            )
            mock_func.return_value = ""

            return mock_func

        def test_when_node_is_empty(self, empty_node):
            assert empty_node.path == ""

        def test_when_parent_has_no_url(self):
            base_path = "http://foo.com"
            node = EndpointNode({"path": base_path}, parent=EndpointNode({}))
            assert node.path == base_path

        def test_when_parent_has_url(self):
            base_path = "http://foo.com/api"
            parent = EndpointNode({"path": base_path})
            node = EndpointNode({"path": "/foo"}, parent=parent)
            assert node.path == f"http://foo.com/api/foo"

        def test_with_trailing_slashes(self):
            parent = EndpointNode({"path": "http://foo.com/"})
            node = EndpointNode({"path": "/foo/"}, parent=parent)
            assert node.path == "http://foo.com/foo/"

        def test_calls_evaluate(self, mocker, mock_evaluate):
            parent = EndpointNode({"path": "http://foo.com/"})
            node = EndpointNode({"path": "/foo/"}, parent=parent)
            node.path
            calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

            mock_evaluate.assert_has_calls(calls)

    class TestHeaders:
        def test_when_node_is_empty(self, empty_node):
            assert empty_node.headers == {}

        def test_when_parent_has_no_headers(self):
            headers = {"abc": "def"}
            node = EndpointNode({"headers": headers}, parent=EndpointNode({}))
            assert node.headers == headers

        def test_when_parent_has_headers(self):
            headers = {"abc": "def"}
            parent_headers = {"xxx": "www"}
            node = EndpointNode(
                {"headers": headers}, parent=EndpointNode({"headers": parent_headers})
            )
            assert node.headers == {"abc": "def", "xxx": "www"}

        def test_when_parent_has_repeated_keys(self):
            headers = {"abc": "def"}
            parent_headers = {"xxx": "www", "abc": "zxc"}
            node = EndpointNode(
                {"headers": headers}, parent=EndpointNode({"headers": parent_headers})
            )
            assert node.headers == {"abc": "def", "xxx": "www"}

    class TestGetRequests:
        def test_when_node_is_empty(self, empty_node):
            requests = list(empty_node._get_requests())
            assert len(requests) == 0

        def test_when_node_has_children(self):
            node = EndpointNode(
                {
                    "endpoints": [
                        {
                            "name": "foo",
                            "requests": [{"name": "First"}, {"name": "Second"}],
                        }
                    ]
                }
            )
            requests = list(node._get_requests())
            assert len(requests) == 2

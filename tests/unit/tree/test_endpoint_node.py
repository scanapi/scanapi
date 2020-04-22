import pytest

from scanapi.tree import EndpointNode


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
                "scanapi.tree.endpoint_node.SpecEvaluator.evaluate"
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

    class TestParams:
        def test_when_node_is_empty(self, empty_node):
            assert empty_node.params == {}

        def test_when_parent_has_no_params(self):
            params = {"abc": "def"}
            node = EndpointNode({"params": params}, parent=EndpointNode({}))
            assert node.params == params

        def test_when_parent_has_params(self):
            params = {"abc": "def"}
            parent_params = {"xxx": "www"}
            node = EndpointNode(
                {"params": params}, parent=EndpointNode({"params": parent_params})
            )
            assert node.params == {"abc": "def", "xxx": "www"}

        def test_when_parent_has_repeated_keys(self):
            params = {"abc": "def"}
            parent_params = {"xxx": "www", "abc": "zxc"}
            node = EndpointNode(
                {"params": params}, parent=EndpointNode({"params": parent_params})
            )
            assert node.params == {"abc": "def", "xxx": "www"}

    class TestRun:
        pass  # TODO

    class TestValidate:
        @pytest.fixture()
        def mock_validate_keys(self, mocker):
            return mocker.patch("scanapi.tree.endpoint_node.validate_keys")

        def test_should_call_validate_keys(self, mock_validate_keys):
            spec = {"headers": {"foo": "bar"}, "name": "foo", "path": "foo.bar"}
            node = EndpointNode(spec)
            keys = spec.keys()
            node._validate()

            mock_validate_keys.assert_called_with(
                keys,
                ("endpoints", "headers", "name", "params", "path", "requests"),
                "endpoint",
            )
            assert len(keys) == 3
            assert "headers" in keys
            assert "name" in keys
            assert "path" in keys

    class TestGetSpecs:
        pass  # TODO

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

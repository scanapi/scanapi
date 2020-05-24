import pytest

from scanapi.tree import EndpointNode
from scanapi.errors import MissingMandatoryKeyError


class TestEndpointNode:
    class TestInit:
        def test_should_create_children(self):
            endpoints = [
                {"name": "child-node-one", "requests": []},
                {"name": "child-node-two", "requests": []},
            ]
            node = EndpointNode(
                {"endpoints": endpoints, "name": "scanapi-demo", "requests": []}
            )
            assert len(node.child_nodes) == len(endpoints)

        def test_missing_required_keys(self):
            with pytest.raises(MissingMandatoryKeyError) as excinfo:
                endpoints = [{}, {}]
                node = EndpointNode({"endpoints": endpoints})

            assert str(excinfo.value) == "Missing 'name' key(s) at 'endpoint' scope"

        def test_no_required_keys_for_root(self):
            assert EndpointNode({})

    class TestName:
        def test_when_parent_has_no_name(self):
            base_path = "http://foo.com"
            node = EndpointNode({"name": "child-node"}, parent=EndpointNode({}))
            assert node.name == "child-node"

        def test_when_parent_has_name(self):
            parent = EndpointNode({"name": "root"})
            node = EndpointNode({"name": "child-node"}, parent=parent)
            assert node.name == "root::child-node"

    class TestPath:
        @pytest.fixture
        def mock_evaluate(self, mocker):
            mock_func = mocker.patch(
                "scanapi.tree.endpoint_node.SpecEvaluator.evaluate"
            )
            mock_func.return_value = ""

            return mock_func

        def test_when_parent_has_no_url(self):
            base_path = "http://foo.com"
            node = EndpointNode(
                {"path": base_path, "name": "child-node", "requests": []},
                parent=EndpointNode({"name": "parent-node", "requests": []}),
            )
            assert node.path == base_path

        def test_when_parent_has_url(self):
            base_path = "http://foo.com/api"
            parent = EndpointNode(
                {"path": base_path, "name": "parent-node", "requests": []}
            )
            node = EndpointNode(
                {"path": "/foo", "name": "node", "requests": []}, parent=parent
            )
            assert node.path == f"http://foo.com/api/foo"

        def test_with_trailing_slashes(self):
            parent = EndpointNode(
                {"path": "http://foo.com/", "name": "parent-node", "requests": []}
            )
            node = EndpointNode(
                {"path": "/foo/", "name": "node", "requests": []}, parent=parent
            )
            assert node.path == "http://foo.com/foo/"

        def test_calls_evaluate(self, mocker, mock_evaluate):
            parent = EndpointNode(
                {"path": "http://foo.com/", "name": "parent-node", "requests": []}
            )
            node = EndpointNode(
                {"path": "/foo/", "name": "node", "requests": []}, parent=parent
            )
            node.path
            calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

            mock_evaluate.assert_has_calls(calls)

    class TestHeaders:
        def test_when_parent_has_no_headers(self):
            headers = {"abc": "def"}
            node = EndpointNode(
                {"headers": headers, "name": "node", "requests": []},
                parent=EndpointNode({"name": "parent-node", "requests": []}),
            )
            assert node.headers == headers

        def test_when_parent_has_headers(self):
            headers = {"abc": "def"}
            parent_headers = {"xxx": "www"}
            node = EndpointNode(
                {"headers": headers, "name": "node", "requests": []},
                parent=EndpointNode(
                    {"headers": parent_headers, "name": "parent-node", "requests": []}
                ),
            )
            assert node.headers == {"abc": "def", "xxx": "www"}

        def test_when_parent_has_repeated_keys(self):
            headers = {"abc": "def"}
            parent_headers = {"xxx": "www", "abc": "zxc"}
            node = EndpointNode(
                {"headers": headers, "name": "node", "requests": []},
                parent=EndpointNode(
                    {"headers": parent_headers, "name": "parent-node", "requests": []}
                ),
            )
            assert node.headers == {"abc": "def", "xxx": "www"}

    class TestParams:
        def test_when_parent_has_no_params(self):
            params = {"abc": "def"}
            node = EndpointNode(
                {"params": params, "name": "node", "requests": []},
                parent=EndpointNode({"name": "parent-node", "requests": []}),
            )
            assert node.params == params

        def test_when_parent_has_params(self):
            params = {"abc": "def"}
            parent_params = {"xxx": "www"}
            node = EndpointNode(
                {"params": params, "name": "node", "requests": []},
                parent=EndpointNode(
                    {"params": parent_params, "name": "parent-node", "requests": []}
                ),
            )
            assert node.params == {"abc": "def", "xxx": "www"}

        def test_when_parent_has_repeated_keys(self):
            params = {"abc": "def"}
            parent_params = {"xxx": "www", "abc": "zxc"}
            node = EndpointNode(
                {"params": params, "name": "node", "requests": []},
                parent=EndpointNode(
                    {"params": parent_params, "name": "parent-node", "requests": []}
                ),
            )
            assert node.params == {"abc": "def", "xxx": "www"}

    class TestRun:
        pass  # TODO

    class TestValidate:
        @pytest.fixture()
        def mock_validate_keys(self, mocker):
            return mocker.patch("scanapi.tree.endpoint_node.validate_keys")

        def test_should_call_validate_keys(self, mock_validate_keys):
            spec = {
                "headers": {"foo": "bar"},
                "name": "foo",
                "path": "foo.bar",
                "requests": [],
            }
            node = EndpointNode(spec, parent=EndpointNode({}))
            keys = spec.keys()
            node._validate()

            mock_validate_keys.assert_called_with(
                keys,
                ("endpoints", "headers", "name", "params", "path", "requests"),
                ("name",),
                "endpoint",
            )
            assert len(keys) == 4
            assert "headers" in keys
            assert "name" in keys
            assert "path" in keys

    class TestGetSpecs:
        pass  # TODO

    class TestGetRequests:
        def test_when_node_has_children(self):
            node = EndpointNode(
                {
                    "endpoints": [
                        {
                            "name": "foo",
                            "requests": [
                                {"name": "First", "path": "http://foo.com/first"},
                                {"name": "Second", "path": "http://foo.com/second"},
                            ],
                        }
                    ],
                    "name": "node",
                    "requests": [],
                }
            )
            requests = list(node._get_requests())
            assert len(requests) == 2

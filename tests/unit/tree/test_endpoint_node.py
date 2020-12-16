import pytest

from scanapi.errors import MissingMandatoryKeyError
from scanapi.tree import EndpointNode


@pytest.mark.describe("Test Endpoint Node")
class TestEndpointNode:
    @pytest.mark.describe("Test Init")
    class TestInit:
        @pytest.mark.it("should_create_children")
        def test_should_create_children(self):
            endpoints = [
                {"name": "child-node-one", "requests": []},
                {"name": "child-node-two", "requests": []},
            ]
            node = EndpointNode(
                {
                    "endpoints": endpoints,
                    "name": "scanapi-demo",
                    "requests": [],
                }
            )
            assert len(node.child_nodes) == len(endpoints)

        @pytest.mark.context("When Required Keys are missing")
        @pytest.mark.it("should raise Missing Mandatory Key Error")
        def test_missing_required_keys(self):
            with pytest.raises(MissingMandatoryKeyError) as excinfo:
                endpoints = [{}, {}]
                EndpointNode({"endpoints": endpoints})

            assert (
                str(excinfo.value)
                == "Missing 'name' key(s) at 'endpoint' scope"
            )

        def test_no_required_keys_for_root(self):
            assert EndpointNode({})

    @pytest.mark.describe("Test Name")
    class TestName:
        @pytest.mark.context("When parent has no name")
        @pytest.mark.it("should set child node's name")
        def test_when_parent_has_no_name(self):
            node = EndpointNode({"name": "child-node"}, parent=EndpointNode({}))
            assert node.name == "child-node"

        @pytest.mark.context("When parent has name")
        @pytest.mark.it("should set parent_name::child_name")
        def test_when_parent_has_name(self):
            parent = EndpointNode({"name": "root"})
            node = EndpointNode({"name": "child-node"}, parent=parent)
            assert node.name == "root::child-node"

    @pytest.mark.describe("Test Path")
    class TestPath:
        @pytest.fixture
        def mock_evaluate(self, mocker):
            mock_func = mocker.patch(
                "scanapi.tree.endpoint_node.SpecEvaluator.evaluate"
            )
            mock_func.return_value = ""

            return mock_func

        @pytest.mark.context("When Parent Has No url")
        def test_when_parent_has_no_url(self):
            base_path = "http://foo.com"
            node = EndpointNode(
                {"path": base_path, "name": "child-node", "requests": []},
                parent=EndpointNode({"name": "parent-node", "requests": []}),
            )
            assert node.path == base_path

        @pytest.mark.context("When Parent Has url")
        def test_when_parent_has_url(self):
            base_path = "http://foo.com/api"
            parent = EndpointNode(
                {"path": base_path, "name": "parent-node", "requests": []}
            )
            node = EndpointNode(
                {"path": "/foo", "name": "node", "requests": []}, parent=parent
            )
            assert node.path == "http://foo.com/api/foo"

        @pytest.mark.context("When URL has trailing slashes")
        def test_with_trailing_slashes(self):
            parent = EndpointNode(
                {
                    "path": "http://foo.com/",
                    "name": "parent-node",
                    "requests": [],
                }
            )
            node = EndpointNode(
                {"path": "/foo/", "name": "node", "requests": []},
                parent=parent,
            )
            assert node.path == "http://foo.com/foo/"

        @pytest.mark.context("When path is not a string")
        def test_with_path_not_string(self):
            parent = EndpointNode(
                {
                    "path": "http://foo.com/",
                    "name": "parent-node",
                    "requests": [],
                }
            )
            node = EndpointNode(
                {"path": 2, "name": "node", "requests": []}, parent=parent
            )
            assert node.path == "http://foo.com/2"

        @pytest.mark.it("should call evaluate")
        def test_calls_evaluate(self, mocker, mock_evaluate):
            parent = EndpointNode(
                {
                    "path": "http://foo.com/",
                    "name": "parent-node",
                    "requests": [],
                }
            )
            node = EndpointNode(
                {"path": "/foo/", "name": "node", "requests": []},
                parent=parent,
            )
            node.path
            calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

            mock_evaluate.assert_has_calls(calls)

    @pytest.mark.describe("Test Headers")
    class TestHeaders:
        @pytest.mark.context("When parent has no headers")
        def test_when_parent_has_no_headers(self):
            headers = {"abc": "def"}
            node = EndpointNode(
                {"headers": headers, "name": "node", "requests": []},
                parent=EndpointNode({"name": "parent-node", "requests": []}),
            )
            assert node.headers == headers

        @pytest.mark.context("When parent has headers")
        def test_when_parent_has_headers(self):
            headers = {"abc": "def"}
            parent_headers = {"xxx": "www"}
            node = EndpointNode(
                {"headers": headers, "name": "node", "requests": []},
                parent=EndpointNode(
                    {
                        "headers": parent_headers,
                        "name": "parent-node",
                        "requests": [],
                    }
                ),
            )
            assert node.headers == {"abc": "def", "xxx": "www"}

        @pytest.mark.context("When parent has repeated keys")
        def test_when_parent_has_repeated_keys(self):
            headers = {"abc": "def"}
            parent_headers = {"xxx": "www", "abc": "zxc"}
            node = EndpointNode(
                {"headers": headers, "name": "node", "requests": []},
                parent=EndpointNode(
                    {
                        "headers": parent_headers,
                        "name": "parent-node",
                        "requests": [],
                    }
                ),
            )
            assert node.headers == {"abc": "def", "xxx": "www"}

    @pytest.mark.describe("Test Params")
    class TestParams:
        @pytest.mark.context("When parent has no params")
        def test_when_parent_has_no_params(self):
            params = {"abc": "def"}
            node = EndpointNode(
                {"params": params, "name": "node", "requests": []},
                parent=EndpointNode({"name": "parent-node", "requests": []}),
            )
            assert node.params == params

        @pytest.mark.context("When parent has params")
        def test_when_parent_has_params(self):
            params = {"abc": "def"}
            parent_params = {"xxx": "www"}
            node = EndpointNode(
                {"params": params, "name": "node", "requests": []},
                parent=EndpointNode(
                    {
                        "params": parent_params,
                        "name": "parent-node",
                        "requests": [],
                    }
                ),
            )
            assert node.params == {"abc": "def", "xxx": "www"}

        @pytest.mark.context("When parent has repeated keys")
        def test_when_parent_has_repeated_keys(self):
            params = {"abc": "def"}
            parent_params = {"xxx": "www", "abc": "zxc"}
            node = EndpointNode(
                {"params": params, "name": "node", "requests": []},
                parent=EndpointNode(
                    {
                        "params": parent_params,
                        "name": "parent-node",
                        "requests": [],
                    }
                ),
            )
            assert node.params == {"abc": "def", "xxx": "www"}

    @pytest.mark.describe("Test Delay")
    class TestDelay:
        @pytest.mark.context("When node has no delay")
        def test_when_node_has_no_delay(self):
            node = EndpointNode({"name": "node"})
            assert node.delay == 0

        @pytest.mark.context("When node has delay")
        def test_when_node_has_delay(self):
            node = EndpointNode({"name": "node", "delay": 1})
            assert node.delay == 1

        @pytest.mark.context("When parent has delay")
        def test_when_parent_has_delay(self):
            node = EndpointNode(
                {"name": "node"},
                parent=EndpointNode({"name": "parent", "delay": 2}),
            )
            assert node.delay == 2

        @pytest.mark.context("When both node and parent have delay")
        def test_when_both_node_and_parent_have_delay(self):
            node = EndpointNode(
                {"name": "node", "delay": 3},
                parent=EndpointNode({"name": "parent", "delay": 4}),
            )
            assert node.delay == 3

    @pytest.mark.describe("Test Run")
    class TestRun:
        pass  # TODO

    @pytest.mark.describe("Test Validate")
    class TestValidate:
        @pytest.fixture()
        def mock_validate_keys(self, mocker):
            return mocker.patch("scanapi.tree.endpoint_node.validate_keys")

        @pytest.mark.it("should call validate keys")
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
                (
                    "endpoints",
                    "headers",
                    "name",
                    "params",
                    "path",
                    "requests",
                    "delay",
                ),
                ("name",),
                "endpoint",
            )
            assert len(keys) == 4
            assert "headers" in keys
            assert "name" in keys
            assert "path" in keys

    @pytest.mark.describe("Test Get Specs")
    class TestGetSpecs:
        pass  # TODO

    @pytest.mark.describe("Test Get Requests")
    class TestGetRequests:
        @pytest.mark.context("When node has children")
        def test_when_node_has_children(self):
            node = EndpointNode(
                {
                    "endpoints": [
                        {
                            "name": "foo",
                            "requests": [
                                {
                                    "name": "First",
                                    "path": "http://foo.com/first",
                                },
                                {
                                    "name": "Second",
                                    "path": "http://foo.com/second",
                                },
                            ],
                        }
                    ],
                    "name": "node",
                    "requests": [],
                }
            )
            requests = list(node._get_requests())
            assert len(requests) == 2

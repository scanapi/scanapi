from pytest import fixture, mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("path")
class TestPath:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.tree.endpoint_node.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when parent spec has no path defined")
    @mark.it("should set the path the same as node path")
    def test_when_parent_has_no_url(self):
        base_path = "http://foo.com"
        node = EndpointNode(
            {"path": base_path, "name": "child-node", "requests": []},
            parent=EndpointNode({"name": "parent-node", "requests": []}),
        )
        assert node.path == base_path

    @mark.context("when parent spec has a path defined")
    @mark.it("should set path as the concatenation of parent and node paths")
    def test_when_parent_has_url(self):
        base_path = "http://foo.com/api"
        parent = EndpointNode(
            {"path": base_path, "name": "parent-node", "requests": []}
        )
        node = EndpointNode(
            {"path": "/foo", "name": "node", "requests": []}, parent=parent
        )
        assert node.path == "http://foo.com/api/foo"

    @mark.context(
        "When parent spec has a path ending with slash and node path beggins with a slash"
    )
    @mark.it(
        "should set path as the concatenation of parent and node paths "
        "without double slashes"
    )
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

    @mark.context("when node spec has a path that is not a string")
    @mark.it("should set path as the concatenation of parent and node paths")
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

    @mark.it("should call the evaluate method")
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

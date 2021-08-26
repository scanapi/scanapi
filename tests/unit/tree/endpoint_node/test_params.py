from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("params")
class TestParams:
    @mark.context("when parent spec has no params attribute defined")
    @mark.it("should set params attribute the same as the node's one")
    def test_when_parent_has_no_params(self):
        params = {"abc": "def"}
        node = EndpointNode(
            {"params": params, "name": "node", "requests": []},
            parent=EndpointNode({"name": "parent-node", "requests": []}),
        )
        assert node.params == params

    @mark.context("when parent has params")
    @mark.context(
        "when both node and parent specs have a params attribute defined"
    )
    @mark.it(
        "should set params attribute the result of merging "
        "the node's and the parent's params"
    )
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

    @mark.context(
        "when both node and parent specs have a params attribute defined with repeated keys"
    )
    @mark.it(
        "should set params attribute the result of merging "
        "the node's and the parent's params with the repeated keys containing "
        "the node's corresponding value"
    )
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

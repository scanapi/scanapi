from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("__repr__")
class TestRepr:
    @mark.context("when parent spec has no name defined")
    @mark.it("should return <EndpointNode child-node>")
    def test_when_parent_has_no_name(self):
        node = EndpointNode({"name": "child-node"}, parent=EndpointNode({}))
        assert repr(node) == "<EndpointNode child-node>"

    @mark.context("when parent spec has a name defined")
    @mark.it("should return <EndpointNode root::child-node>")
    def test_when_parent_has_name(self):
        parent = EndpointNode({"name": "root"})
        node = EndpointNode({"name": "child-node"}, parent=parent)
        assert repr(node) == "<EndpointNode root::child-node>"

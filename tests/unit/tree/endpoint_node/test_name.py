from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("name")
class TestName:
    @mark.context("when parent spec has no name defined")
    @mark.it("should set child node's name")
    def test_when_parent_has_no_name(self):
        node = EndpointNode({"name": "child-node"}, parent=EndpointNode({}))
        assert node.name == "child-node"

    @mark.context("when parent spec has a name defined")
    @mark.it("should set parent_name::child_name")
    def test_when_parent_has_name(self):
        parent = EndpointNode({"name": "root"})
        node = EndpointNode({"name": "child-node"}, parent=parent)
        assert node.name == "root::child-node"

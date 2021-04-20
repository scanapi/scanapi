from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("delay")
class TestDelay:
    @mark.context("when node spec has no delay defined")
    @mark.it("should set delay as 0")
    def test_when_node_has_no_delay(self):
        node = EndpointNode({"name": "node"})
        assert node.delay == 0

    @mark.context("when node spec has a delay defined")
    @mark.it("should set delay attribute accordingly")
    def test_when_node_has_delay(self):
        node = EndpointNode({"name": "node", "delay": 1})
        assert node.delay == 1

    @mark.context("when parent node spec has a delay defined")
    @mark.it("should set delay attribute the same as the parent's one")
    def test_when_parent_has_delay(self):
        node = EndpointNode(
            {"name": "node"},
            parent=EndpointNode({"name": "parent", "delay": 2}),
        )
        assert node.delay == 2

    @mark.context("when both node and parent specs have a delay defined")
    @mark.it("should set delay attribute the same as the node's one")
    def test_when_both_node_and_parent_have_delay(self):
        node = EndpointNode(
            {"name": "node", "delay": 3},
            parent=EndpointNode({"name": "parent", "delay": 4}),
        )
        assert node.delay == 3

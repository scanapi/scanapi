from pytest import mark, raises

from scanapi.errors import MissingMandatoryKeyError
from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("__init__")
class TestInit:
    @mark.context("when there are no mandatory keys missing")
    @mark.it("should create children")
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

    @mark.context("when required keys are missing")
    @mark.it("should raise missing mandatory key error")
    def test_missing_required_keys(self):
        with raises(MissingMandatoryKeyError) as excinfo:
            endpoints = [{}, {}]
            EndpointNode({"endpoints": endpoints})

        assert str(excinfo.value) == "Missing 'name' key(s) at 'endpoint' scope"

    @mark.it("should not raise missing mandatory key error for root node")
    def test_no_required_keys_for_root(self):
        assert EndpointNode({})

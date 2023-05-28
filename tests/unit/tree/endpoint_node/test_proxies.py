from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("proxies")
class TestProxies:
    @mark.context("when parent spec has no proxies defined")
    @mark.it("should have only node proxies")
    def test_when_parent_has_no_proxies(self):
        proxies = {"all://": "http://localhost:123"}

        node = EndpointNode(
            {"name": "child-node", "proxies": proxies},
            parent=EndpointNode({"name": "root"}),
        )

        assert node.proxies == proxies

    @mark.context("when parent and node spec has  defined")
    @mark.it("should keep node proxies")
    def test_when_both_was_same_proxies(self):
        parent_proxies = {"all://": "http://localhost:123"}
        child_proxies = "https://0.0.0.0:321"

        parent = EndpointNode({"name": "root", "proxies": parent_proxies})
        node = EndpointNode(
            {"name": "child-node", "proxies": child_proxies}, parent=parent
        )

        assert node.proxies == child_proxies

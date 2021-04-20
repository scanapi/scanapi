from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("headers")
class TestHeaders:
    @mark.context("when parent spec has no headers attribute defined")
    @mark.it("should set headers attribute the same as the node's one")
    def test_when_parent_has_no_headers(self):
        headers = {"abc": "def"}
        node = EndpointNode(
            {"headers": headers, "name": "node", "requests": []},
            parent=EndpointNode({"name": "parent-node", "requests": []}),
        )
        assert node.headers == headers

    @mark.context(
        "when both node and parent specs have a headers attribute defined"
    )
    @mark.it(
        "should set headers attribute the result of merging "
        "the node's and the parent's headers"
    )
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

    @mark.context(
        "when both node and parent specs have a headers attribute defined with repeated keys"
    )
    @mark.it(
        "should set headers attribute the result of merging "
        "the node's and the parents' headers with the repeated keys containing "
        "the node's corresponding value"
    )
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

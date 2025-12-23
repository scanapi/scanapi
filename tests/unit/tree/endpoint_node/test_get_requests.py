from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("_get_requests")
class TestGetRequests:
    @mark.context("when node has children")
    @mark.it("should return the requests")
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

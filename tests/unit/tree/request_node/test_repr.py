from pytest import mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("__repr__")
class TestRepr:
    @mark.context("when path is not defined")
    @mark.it("should return <RequestNode >")
    def test_when_path_is_not_defined(self):
        endpoint = EndpointNode({"name": "foo", "requests": [{}]})
        request = RequestNode(spec={"name": "bar"}, endpoint=endpoint)
        assert repr(request) == "<RequestNode >"

    @mark.context("when endpoint node path is defined")
    @mark.it("should return <RequestNode endpoint_path>")
    def test_when_endpoint_path_is_defined(self):
        base_path = "http://foo.com/api"
        parent = EndpointNode(
            {"path": base_path, "name": "parent-node", "requests": []}
        )
        endpoint = EndpointNode(
            {"path": "/foo", "name": "node", "requests": []}, parent=parent
        )

        request = RequestNode(spec={"name": "bar"}, endpoint=endpoint)
        assert repr(request) == "<RequestNode http://foo.com/api/foo>"

    @mark.context("when request node path is defined")
    @mark.it("should return <RequestNode request_path>")
    def test_when_request_node_path_is_defined(self):
        endpoint = EndpointNode({"name": "foo", "requests": [{}]})
        request = RequestNode(
            spec={"name": "bar", "path": "/bar/"}, endpoint=endpoint
        )
        assert repr(request) == "<RequestNode /bar/>"

    @mark.context("when both request and endpoint paths are defined")
    @mark.it("should return <RequestNode endpoint_path/request_path>")
    def test_when_request_and_endpoint_paths_are_defined(self):
        base_path = "http://foo.com/api"
        parent = EndpointNode(
            {"path": base_path, "name": "parent-node", "requests": []}
        )
        endpoint = EndpointNode(
            {"path": "/foo", "name": "node", "requests": []}, parent=parent
        )

        request = RequestNode(
            spec={"name": "bar", "path": "/bar/"}, endpoint=endpoint
        )
        assert repr(request) == "<RequestNode http://foo.com/api/foo/bar/>"

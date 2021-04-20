from pytest import mark, raises

from scanapi.errors import HTTPMethodNotAllowedError
from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("http_method")
class TestHTTPMethod:
    @mark.context("when request spec has an http method defined")
    @mark.it("should set the http_method attribute accordingly")
    def test_when_request_has_method(self):
        request = RequestNode(
            {"method": "put", "name": "foo", "path": "http:foo.com"},
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        assert request.http_method == "PUT"

    @mark.context("when request spec has no http method defined")
    @mark.it("should set the http_method attribute as get")
    def test_when_request_has_no_method(self):
        request = RequestNode(
            {"name": "foo", "path": "http:foo.com"},
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        assert request.http_method == "GET"

    @mark.context("when request spec has and invalid http method defined")
    @mark.it("should raise http method not allowed error")
    def test_when_method_is_invalid(self):
        request = RequestNode(
            {"method": "XXX", "name": "foo", "path": "http:foo.com"},
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        with raises(HTTPMethodNotAllowedError) as excinfo:
            request.http_method

        expected = (
            f"HTTP method not supported: {request.spec.get('method')}."
            f" Supported methods: {request.ALLOWED_HTTP_METHODS}."
        )
        assert str(excinfo.value) == expected

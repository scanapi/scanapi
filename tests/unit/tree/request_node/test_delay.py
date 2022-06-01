from pytest import mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("delay")
class TestDelay:
    @mark.context("when request spec has no delay defined")
    @mark.it("should set delay as 0")
    def test_when_request_has_no_delay(self):
        request = RequestNode(
            {"name": "foo"}, endpoint=EndpointNode({"name": "bar"})
        )
        assert request.delay == 0

    @mark.context("when request spec has a delay defined")
    @mark.it("should set delay attribute accordingly")
    def test_when_request_has_delay(self):
        request = RequestNode(
            {"name": "foo", "delay": 1},
            endpoint=EndpointNode({"name": "bar"}),
        )
        assert request.delay == 1

    @mark.context("when endpoint spec has a delay defined")
    @mark.it("should set delay attribute the same as the endpoint's one")
    def test_when_endpoint_has_delay(self):
        request = RequestNode(
            {"name": "foo"},
            endpoint=EndpointNode({"name": "bar", "delay": 2}),
        )
        assert request.delay == 2

    @mark.context("when both request and endpoint specs have a delay defined")
    @mark.it("should set delay attribute the same as the request's one")
    def test_when_both_request_and_endpoint_have_delay(self):
        request = RequestNode(
            {"name": "foo", "delay": 3},
            endpoint=EndpointNode({"name": "bar", "delay": 4}),
        )
        assert request.delay == 3

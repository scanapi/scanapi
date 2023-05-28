from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("proxies")
class TestProxies:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.tree.request_node.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when request spec has a proxies defined")
    @mark.it("should set the proxies attribute accordingly")
    def test_when_request_has_proxies(self):
        proxies = {"http://": "http://localhost:123"}
        request = RequestNode(
            {"name": "list-users", "path": "http:foo.com", "proxies": proxies},
            endpoint=EndpointNode({"name": "foo", "requests": []}),
        )

        assert request.proxies == proxies

    @mark.context(
        "when request and enpoint spec has a proxies with same keys defined"
    )
    @mark.it("should priorize the proxies attribute values of request")
    def test_when_request_and_endpoint_has_proxies(self):
        endpoint_proxies = {"all://": "http://localhost:123"}
        request_proxies = {"http://": "http://localhost:321"}

        request = RequestNode(
            {
                "name": "list-users",
                "path": "http:foo.com",
                "proxies": request_proxies,
            },
            endpoint=EndpointNode(
                {"name": "foo", "proxies": endpoint_proxies, "requests": []}
            ),
        )

        assert request.proxies == request_proxies

from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("headers")
class TestHeaders:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when endpoint spec has no headers attribute defined")
    @mark.it("should set headers attribute the same as the request's one")
    def test_when_endpoint_has_no_headers(self):
        headers = {"abc": "def"}
        request = RequestNode(
            {"headers": headers, "path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        assert request.headers == headers

    @mark.context(
        "when both request and endpoint specs have a headers attribute defined"
    )
    @mark.it(
        "should set headers attribute the result of merging "
        "the endpoint's and the request's headers"
    )
    def test_when_endpoint_has_headers(self):
        headers = {"abc": "def"}
        endpoint_headers = {"xxx": "www"}
        request = RequestNode(
            {"headers": headers, "path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode(
                {
                    "headers": endpoint_headers,
                    "name": "foo",
                    "requests": [{}],
                }
            ),
        )
        assert request.headers == {"abc": "def", "xxx": "www"}

    @mark.context(
        "when both request and endpoint specs have a headers attribute defined with repeated keys"
    )
    @mark.it(
        "should set headers attribute the result of merging "
        "the endpoint's and the request's headers with the repeated keys containing "
        "the request's corresponding value"
    )
    def test_with_repeated_keys(self):
        headers = {"abc": "def"}
        endpoint_headers = {"xxx": "www", "abc": "zxc"}
        request = RequestNode(
            {"headers": headers, "path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode(
                {
                    "headers": endpoint_headers,
                    "name": "foo",
                    "requests": [{}],
                }
            ),
        )
        assert request.headers == {"abc": "def", "xxx": "www"}

    @mark.context("when request spec has a headers attribute defined")
    @mark.it("should call the evaluate method")
    def test_calls_evaluate(self, mocker, mock_evaluate):
        endpoint = EndpointNode(
            {"headers": {"abc": "def"}, "name": "foo", "requests": [{}]}
        )

        request = RequestNode(
            {
                "headers": {"ghi": "jkl"},
                "path": "http://foo.com",
                "name": "foo",
            },
            endpoint=endpoint,
        )
        request.headers
        calls = [mocker.call({"abc": "def", "ghi": "jkl"})]

        mock_evaluate.assert_has_calls(calls)

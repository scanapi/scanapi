from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("params")
class TestParams:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when endpoint spec has no params attribute defined")
    @mark.it("should set params attribute the same as the request's one")
    def test_when_endpoint_has_no_params(self):
        params = {"abc": "def"}
        request = RequestNode(
            {"params": params, "path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        assert request.params == params

    @mark.context(
        "when both request and endpoint specs have a params attribute defined"
    )
    @mark.it(
        "should set params attribute the result of merging "
        "the endpoint's and the request's params"
    )
    def test_when_endpoint_has_params(self):
        params = {"abc": "def"}
        endpoint_params = {"xxx": "www"}
        request = RequestNode(
            {"params": params, "path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode(
                {
                    "params": endpoint_params,
                    "name": "foo",
                    "requests": [{}],
                }
            ),
        )
        assert request.params == {"abc": "def", "xxx": "www"}

    @mark.context(
        "when both request and endpoint specs have a params attribute defined with repeated keys"
    )
    @mark.it(
        "should set params attribute the result of merging "
        "the endpoint's and the request's params with the repeated keys containing "
        "the request's corresponding value"
    )
    def test_with_repeated_keys(self):
        params = {"abc": "def"}
        endpoint_params = {"xxx": "www", "abc": "zxc"}
        request = RequestNode(
            {"params": params, "path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode(
                {
                    "params": endpoint_params,
                    "name": "foo",
                    "requests": [{}],
                }
            ),
        )
        assert request.params == {"abc": "def", "xxx": "www"}

    @mark.context("when request spec has a params attribute defined")
    @mark.it("should call the evaluate method")
    def test_calls_evaluate(self, mocker, mock_evaluate):
        endpoint = EndpointNode(
            {"params": {"abc": "def"}, "name": "foo", "requests": [{}]}
        )

        request = RequestNode(
            {
                "params": {"ghi": "jkl"},
                "path": "http://foo.com",
                "name": "foo",
            },
            endpoint=endpoint,
        )
        request.params
        calls = [mocker.call({"abc": "def", "ghi": "jkl"})]

        mock_evaluate.assert_has_calls(calls)

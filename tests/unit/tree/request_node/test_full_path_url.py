from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("full_url_path")
class TestFullPathUrl:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when endpoint spec has no url defined")
    @mark.it("should set full url path the same as request path")
    def test_when_endpoint_has_no_url(self):
        path = "http://foo.com"
        request = RequestNode(
            {"name": "foo", "path": path},
            endpoint=EndpointNode(
                {"name": "foo", "requests": [{}], "path": ""}
            ),
        )
        assert request.full_url_path == path

    @mark.context("when endpoint spec has an url defined")
    @mark.it(
        "should set full url path as the concatenation of endpoint and request paths"
    )
    def test_when_endpoint_has_url(self):
        endpoint_path = "http://foo.com/api"
        endpoint = EndpointNode(
            {"name": "foo", "requests": [{}], "path": endpoint_path}
        )
        request = RequestNode(
            {"path": "/foo", "name": "foo"}, endpoint=endpoint
        )
        assert request.full_url_path == "http://foo.com/api/foo"

    @mark.context(
        "When endpoint spec has an url ending with slash and request url beggins with a slash"
    )
    @mark.it(
        "should set full url path as the concatenation of endpoint and request paths "
        "without double slashes"
    )
    def test_with_trailing_slashes(self):
        endpoint = EndpointNode(
            {"name": "foo", "requests": [{}], "path": "http://foo.com/"}
        )
        request = RequestNode(
            {"name": "foo", "path": "/foo/"}, endpoint=endpoint
        )
        assert request.full_url_path == "http://foo.com/foo/"

    @mark.context("when request spec has an url that is not a string")
    @mark.it(
        "should set full url path as the concatenation of endpoint and request paths"
    )
    def test_with_path_not_string(self):
        endpoint = EndpointNode(
            {"name": "foo", "requests": [{}], "path": "http://foo.com/"}
        )
        request = RequestNode({"name": "foo", "path": []}, endpoint=endpoint)
        assert request.full_url_path == "http://foo.com/[]"

    @mark.context(
        "when the request specification has a URL that uses a custom variable"
    )
    @mark.it(
        "should set the full url path as the concatenation of the custom variable "
    )
    def test_with_path_custom_var(self):
        endpoint = EndpointNode(
            {"name": "foo", "requests": [{}], "path": "http://foo.com/"}
        )
        request = RequestNode(
            {"name": "foo", "path": "/${bar}", "vars": {"bar": "foo-bar"}},
            endpoint=endpoint,
        )
        assert request.full_url_path == "http://foo.com/foo-bar"

    @mark.it("should call the evaluate method")
    def test_calls_evaluate(self, mocker, mock_evaluate):
        endpoint = EndpointNode(
            {"name": "foo", "requests": [{}], "path": "http://foo.com/"}
        )
        request = RequestNode(
            {"path": "/foo/", "name": "foo"}, endpoint=endpoint
        )
        request.full_url_path
        calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

        mock_evaluate.assert_has_calls(calls)

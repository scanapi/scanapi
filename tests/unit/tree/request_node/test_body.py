from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("body")
class TestBody:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when request spec has no body defined")
    @mark.it("should set body as none")
    def test_when_request_has_no_body(self):
        request = RequestNode(
            {"path": "http://foo.com", "name": "foo"},
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        assert request.body is None

    @mark.context("when request spec has a body defined")
    @mark.it("should set body attribute accordingly")
    def test_when_request_has_body(self):
        request = RequestNode(
            {
                "body": {"abc": "def"},
                "path": "http://foo.com",
                "name": "foo",
            },
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        assert request.body == {"abc": "def"}

    @mark.context("when request spec has a body defined")
    @mark.it("should call the evaluate method")
    def test_calls_evaluate(self, mocker, mock_evaluate):
        request = RequestNode(
            {
                "body": {"ghi": "jkl"},
                "path": "http://foo.com",
                "name": "foo",
            },
            endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
        )
        request.body
        calls = [mocker.call({"ghi": "jkl"})]

        mock_evaluate.assert_has_calls(calls)

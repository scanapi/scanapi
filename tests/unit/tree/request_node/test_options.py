from pytest import fixture, mark, raises

from scanapi.errors import InvalidKeyError
from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("name")
class TestOptions:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.tree.request_node.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when request spec has a options defined")
    @mark.it("should set the options attribute accordingly")
    def test_when_request_has_options(self):
        options = {"timeout": 1.1}
        request = RequestNode(
            {"name": "list-users", "path": "http:foo.com", "options": options},
            endpoint=EndpointNode({"name": "foo", "requests": []}),
        )

        assert request.options == options

    @mark.context(
        "when request and enpoint spec has a options with same keys defined"
    )
    @mark.it("should priorize the options attribute values of request")
    def test_when_request_and_endpoint_has_options(self):
        endpoint_options = {"timeout": 1.2}
        request_options = {"timeout": 1.3}

        request = RequestNode(
            {
                "name": "list-users",
                "path": "http:foo.com",
                "options": request_options,
            },
            endpoint=EndpointNode(
                {"name": "foo", "options": endpoint_options, "requests": []}
            ),
        )

        assert request.options == request_options

    @mark.context("when request spec has and invalid options key defined")
    @mark.it("should raise an exception")
    def test_when_request_option_has_invalid_key(self):
        request = RequestNode(
            {
                "name": "list-users",
                "path": "http:foo.com",
                "options": {"foo": "bar"},
            },
            endpoint=EndpointNode({"name": "foo", "requests": []}),
        )

        with raises(InvalidKeyError) as excinfo:
            request.options

        expected = (
            f"Invalid key 'foo' at 'options' scope. "
            f"Available keys are: {request.ALLOWED_OPTIONS}"
        )

        assert str(excinfo.value) == expected

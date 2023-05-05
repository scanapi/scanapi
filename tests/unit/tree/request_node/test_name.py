from pytest import fixture, mark, raises

from scanapi.errors import MissingMandatoryKeyError
from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("name")
class TestName:
    @fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.tree.request_node.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    @mark.context("when request spec has a name defined")
    @mark.it("should set the name attribute accordingly")
    def test_when_request_has_name(self):
        request = RequestNode(
            {"name": "list-users", "path": "http:foo.com"},
            endpoint=EndpointNode({"name": "foo", "requests": []}),
        )
        assert request.name == "list-users"

    @mark.it("it should validate mandatory `name` key before")
    def test_when_request_has_no_name(self):
        with raises(MissingMandatoryKeyError) as excinfo:
            RequestNode(
                {}, endpoint=EndpointNode({"name": "foo", "requests": []})
            )

        assert str(excinfo.value) == "Missing 'name' key(s) at 'request' scope"

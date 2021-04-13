from pytest import mark, raises

from scanapi.errors import MissingMandatoryKeyError
from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("__init__")
class TestInit:
    @mark.context("when there are no mandatory keys missing")
    @mark.it("should set endpoint and spec attributes accordingly")
    def test_init_spec_and_endpoint(self):
        endpoint = EndpointNode({"name": "foo", "requests": [{}]})
        request = RequestNode(spec={"name": "bar"}, endpoint=endpoint)

        assert request.endpoint == endpoint
        assert request.spec == {"name": "bar"}

    @mark.context("when required keys are missing")
    @mark.it("should raise missing mandatory key error")
    def test_missing_required_keys(self):
        with raises(MissingMandatoryKeyError) as excinfo:
            RequestNode(
                spec={},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )

        assert str(excinfo.value) == "Missing 'name' key(s) at 'request' scope"

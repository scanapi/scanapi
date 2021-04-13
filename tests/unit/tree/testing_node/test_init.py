from pytest import mark, raises

from scanapi.errors import MissingMandatoryKeyError
from scanapi.tree import EndpointNode, RequestNode, TestingNode


@mark.describe("testing node")
@mark.describe("__init__")
class TestInit:
    @mark.context("when required keys are missing")
    @mark.it("should raise missing mandatory key error")
    def test_missing_required_keys(self):
        with raises(MissingMandatoryKeyError) as excinfo:
            request_node = RequestNode(
                spec={"name": "foo", "path": "bar"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            TestingNode(spec={}, request=request_node)

        assert (
            str(excinfo.value)
            == "Missing 'assert', 'name' key(s) at 'test' scope"
        )

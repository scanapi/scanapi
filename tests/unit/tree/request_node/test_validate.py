from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode, tree_keys


@mark.describe("request node")
@mark.describe("_validate")
class TestValidate:
    @fixture
    def mock_validate_keys(self, mocker):
        return mocker.patch("scanapi.tree.request_node.validate_keys")

    @mark.it("should call the validate_keys method")
    def test_should_call_validate_keys(self, mock_validate_keys):
        spec = {
            "headers": {"foo": "bar"},
            "name": "foo",
            "path": "foo.bar",
        }
        node = RequestNode(
            spec, endpoint=EndpointNode({"name": "foo", "requests": [{}]})
        )
        keys = spec.keys()
        node._validate()

        mock_validate_keys.assert_called_with(
            keys,
            (
                "body",
                "headers",
                "method",
                "name",
                "params",
                "path",
                "tests",
                tree_keys.VARS_KEY,
                "delay",
                "retry",
            ),
            ("name",),
            "request",
        )
        assert len(keys) == 3
        assert "headers" in keys
        assert "name" in keys
        assert "path" in keys

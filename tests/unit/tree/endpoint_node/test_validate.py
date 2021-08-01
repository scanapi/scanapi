from pytest import fixture, mark

from scanapi.tree import EndpointNode, tree_keys


@mark.describe("endpoint node")
@mark.describe("_validate")
class TestValidate:
    @fixture()
    def mock_validate_keys(self, mocker):
        return mocker.patch("scanapi.tree.endpoint_node.validate_keys")

    @mark.it("should call the validate_keys method")
    def test_should_call_validate_keys(self, mock_validate_keys):
        spec = {
            "headers": {"foo": "bar"},
            "name": "foo",
            "path": "foo.bar",
            "requests": [],
        }
        node = EndpointNode(spec, parent=EndpointNode({}))
        keys = spec.keys()
        node._validate()

        mock_validate_keys.assert_called_with(
            keys,
            (
                "endpoints",
                "headers",
                "name",
                "params",
                "path",
                "requests",
                "delay",
                tree_keys.VARS_KEY,
            ),
            ("name",),
            "endpoint",
        )
        assert len(keys) == 4
        assert "headers" in keys
        assert "name" in keys
        assert "path" in keys

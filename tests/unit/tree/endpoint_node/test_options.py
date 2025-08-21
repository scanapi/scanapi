from pytest import mark, raises

from scanapi.errors import InvalidKeyError
from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("options")
class TestOptions:
    @mark.context("when parent spec has no options defined")
    @mark.it("should have only node options")
    def test_when_parent_has_no_options(self):
        options = {"verify": False}

        node = EndpointNode(
            {"name": "child-node", "options": options},
            parent=EndpointNode({"name": "root"}),
        )

        assert node.options == options

    @mark.context("when parent spec has options defined")
    @mark.it("should append parent options")
    def test_when_parent_has_name(self):
        parent_options = {"timeout": 1.0}
        child_options = {"timeout": 2.0}

        parent = EndpointNode({"name": "root", "options": parent_options})
        node = EndpointNode(
            {"name": "child-node", "options": child_options}, parent=parent
        )

        assert node.options == {**parent_options, **child_options}

    @mark.context("when parent and node spec has options defined")
    @mark.it("should keep node options")
    def test_when_both_was_same_options(self):
        parent_options = {"timeout": 1.0}
        child_options = {"timeout": 2.0}

        parent = EndpointNode({"name": "root", "options": parent_options})
        node = EndpointNode(
            {"name": "child-node", "options": child_options}, parent=parent
        )

        assert node.options == child_options

    @mark.context("when node spec has and invalid options key defined")
    @mark.it("should raise an exception")
    def test_when_request_option_has_invalid_key(self):
        node = EndpointNode(
            {
                "name": "root",
                "options": {"foo": "bar"},
            },
        )

        with raises(InvalidKeyError) as excinfo:
            node.options

        expected = (
            f"Invalid key 'foo' at 'options' scope. "
            f"Available keys are: {node.ALLOWED_OPTIONS}"
        )

        assert str(excinfo.value) == expected

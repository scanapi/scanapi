from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("_get_specs")
class TestGetSpecs:
    @mark.context("when both parent and child have the requested spec")
    @mark.it("should return parent and child specs")
    def test_when_parent_and_child_have_same_spec(self):
        spec = {
            "headers": {"child_foo": "child_bar"},
            "name": "node",
            "requests": [],
        }

        parent = EndpointNode(
            {
                "headers": {"parent_foo": "parent_bar"},
                "name": "node",
                "requests": [],
            }
        )

        node = EndpointNode(spec, parent,)

        specs = node._get_specs("headers")

        assert specs == {"parent_foo": "parent_bar", "child_foo": "child_bar"}

    @mark.context("when parent has the requested spec but child does not")
    @mark.it("should return parent spec")
    def test_when_parent_has_spec(self):
        spec = {"name": "node", "requests": []}

        parent = EndpointNode(
            {
                "headers": {"parent_foo": "parent_bar"},
                "name": "node",
                "requests": [],
            }
        )

        node = EndpointNode(spec, parent,)

        specs = node._get_specs("headers")

        assert specs == {"parent_foo": "parent_bar"}

    @mark.context("when child has the requested spec but parent does not")
    @mark.it("should return child spec")
    def test_when_child_has_spec(self):
        spec = {
            "headers": {"child_foo": "child_bar"},
            "name": "node",
            "requests": [],
        }

        parent = EndpointNode({"name": "node", "requests": []})

        node = EndpointNode(spec, parent,)

        specs = node._get_specs("headers")

        assert specs == {"child_foo": "child_bar"}

    @mark.context("when both parent and child do not have the requested spec")
    @mark.it("should return an empty dictionary")
    def test_when_there_is_no_spec(self):
        spec = {"name": "node", "requests": []}

        parent = EndpointNode({"name": "node", "requests": []})

        node = EndpointNode(spec, parent,)

        specs = node._get_specs("headers")

        assert specs == {}

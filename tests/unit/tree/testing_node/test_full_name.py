from pytest import mark

from scanapi.tree import EndpointNode, RequestNode, TestingNode


@mark.describe("testing node")
@mark.describe("full_name")
class TestFullName:
    @mark.it(
        "should set the full_name attribute as the concatanation of the parents' names separated by ::"
    )
    def test_full_name(self):
        endpoint_node = EndpointNode({"name": "foo"})
        request_node = RequestNode(spec={"name": "bar"}, endpoint=endpoint_node)
        test_node = TestingNode(
            spec={"name": "lol", "assert": "okay"}, request=request_node
        )

        assert test_node.full_name == "foo::bar::lol"

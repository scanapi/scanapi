from tests.unit.factories import APITreeFactory


class TestRequestNode:
    class TestDefineTests:
        def test_should_define_tests(self):
            api = APITreeFactory(with_endpoints_with_root_requests=True)
            for request_node in api.request_nodes:
                assert request_node.tests == [
                    {"status_code_is_200": "response.status_code == 200"}
                ]

        def test_should_define_multiple_tests(self):
            api = APITreeFactory(with_multiple_tests=True)
            request_node = api.request_nodes[0]
            assert request_node.tests == [
                {"status_code_is_200": "response.status_code == 200"},
                {"status_code_is_not_201": "response.status_code != 201"},
            ]

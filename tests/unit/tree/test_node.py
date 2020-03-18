import os
import pytest

from scanapi.errors import BadConfigurationError
from scanapi.tree import EndpointNode, RequestNode, StringEvaluator


class TestEndpointNode:
    class TestInit:
        class TestChildNodes:
            def test_should_create_children(self):
                endpoints = [{}, {}]
                node = EndpointNode({"endpoints": endpoints})
                assert len(node.child_nodes) == len(endpoints)

    class TestRootNode:
        node = EndpointNode({})

        def test_path(self):
            assert self.node.path == ""

        def test_namespace(self):
            assert self.node.namespace == "root"

        def test_count_total_requests_zero(self):
            requests = list(self.node.get_requests())
            assert len(requests) == 0

    class TestNodeWithChildren:
        node = EndpointNode(
            {
                "endpoints": [
                    {
                        "namespace": "foo",
                        "requests": [{"namespace": "First"}, {"namespace": "Second"}],
                    }
                ]
            }
        )

        def test_request_request_child_requests(self):
            requests = list(self.node.get_requests())
            assert len(requests) == 2

        def test_path_parent_with_no_url(self):
            base_path = "http://foo.com"
            node = EndpointNode({"path": base_path}, parent=EndpointNode({}))
            assert node.path == base_path

        def test_path_with_parent_url(self):
            base_path = "http://foo.com/api"
            parent = EndpointNode({"path": base_path})
            node = EndpointNode({"path": "/foo"}, parent=parent)
            assert node.path == f"{base_path}/foo"

        def test_path_with_trailing_slashes(self):
            parent = EndpointNode({"path": "http://foo.com/"})
            node = EndpointNode({"path": "/foo/"}, parent=parent)
            assert node.path == "http://foo.com/foo/"


class TestRequestNode:
    def test_request_with_no_path(self):
        base_path = "http://foo.com/"
        request = RequestNode({}, endpoint=EndpointNode({"path": base_path}))
        assert request.full_url_path == base_path


class TestStringEvaluator:
    class TestEvaluateEnvVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no env var", "${var}", "${MyVar}", "${{var}}", "${{VAR}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert StringEvaluator().evaluate_env_var(sequence) == sequence

        class TestWhenMatchesThePattern:
            class TestWhenEnvVarIsSetProperly:
                @pytest.fixture(autouse=True)
                def base_url_env(self):
                    os.environ["BASE_URL"] = "https://jsonplaceholder.typicode.com"
                    os.environ["POST_ID"] = "2"

                test_data = [
                    ("${BASE_URL}", "https://jsonplaceholder.typicode.com"),
                    ("${BASE_URL}/posts", "https://jsonplaceholder.typicode.com/posts"),
                    (
                        "https://jsonplaceholder.typicode.com/posts/${POST_ID}",
                        "https://jsonplaceholder.typicode.com/posts/2",
                    ),
                    (
                        "${BASE_URL}/posts/${POST_ID}",
                        "https://jsonplaceholder.typicode.com/posts/2",
                    ),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_evaluated_var(self, sequence, expected):
                    assert StringEvaluator().evaluate_env_var(sequence) == expected

            class TestWhenThereIsNoCorrespondingEnvVar:
                @pytest.fixture(autouse=True)
                def remove_base_url_env(self):
                    if os.environ.get("BASE_URL"):
                        del os.environ["BASE_URL"]

                def test_should_raise_bad_configuration_error(self):
                    with pytest.raises(BadConfigurationError) as excinfo:
                        StringEvaluator().evaluate_env_var("${BASE_URL}")

                    assert (
                        str(excinfo.value)
                        == "'BASE_URL' environment variable not set or badly configured"
                    )

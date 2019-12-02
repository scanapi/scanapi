import pytest

from scanapi.errors import HTTPMethodNotAllowedError
from tests.unit.factories import APITreeFactory, RequestsMakerFactory


class TestRequestsMaker:
    class TestMakeAll:
        class TestWhenMakeRequestRaisesException:
            @pytest.fixture
            def api_tree(self):
                return APITreeFactory(without_endpoints_minimal=True)

            def test_should_log_the_error_and_not_save_response(self, api_tree, caplog):
                requests_maker = RequestsMakerFactory(api_tree=api_tree)
                request_node = requests_maker.api_tree.request_nodes[0]
                request_node.url = "not an url"
                requests_maker.make_all()

                assert (
                    "Error to make request `list_all_posts`. Invalid URL 'not an url': "
                    "No schema supplied. Perhaps you meant http://not an url?\n"
                    in caplog.text
                )
                assert len(api_tree.responses) == 0

        def test_should_evaluate_requests(self):
            # TODO
            pass

        def test_should_save_responses(self):
            # TODO
            pass

        def test_should_save_custom_vars(self):
            # TODO
            pass

    class TestMakeRequest:
        class TestWhenHTTPMethodIsNotAllowed:
            @pytest.fixture
            def api_tree(self):
                return APITreeFactory(method_not_allowed=True)

            def test_should_raise_http_method_not_allowed_error(self, api_tree):
                requests_maker = RequestsMakerFactory(api_tree=api_tree)
                request_node = requests_maker.api_tree.request_nodes[0]
                with pytest.raises(HTTPMethodNotAllowedError) as excinfo:
                    requests_maker.make_request(request_node)

                assert (
                    str(excinfo.value)
                    == "HTTP method not supported: PET. Supported methods: "
                    "('GET', 'POST', 'PUT', 'DELETE')."
                )

        class TestWhenHTTPMethodIsValid:
            def test_should_build_http_request(self):
                # TODO
                pass

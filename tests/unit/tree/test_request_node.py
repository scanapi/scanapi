import pytest

from scanapi.errors import HTTPMethodNotAllowedError, MissingMandatoryKeyError
from scanapi.tree import EndpointNode, RequestNode


class TestRequestNode:
    @pytest.fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch("scanapi.tree.request_node.SpecEvaluator.evaluate")
        mock_func.return_value = ""

        return mock_func

    class TestInit:
        def test_init_spec_and_endpoint(self):
            endpoint = EndpointNode({"name": "foo", "requests": [{}]})
            request = RequestNode(spec={"name": "bar"}, endpoint=endpoint)

            assert request.endpoint == endpoint
            assert request.spec == {"name": "bar"}

        def test_missing_required_keys(self):
            with pytest.raises(MissingMandatoryKeyError) as excinfo:
                request = RequestNode(
                    spec={}, endpoint=EndpointNode({"name": "foo", "requests": [{}]})
                )

            assert str(excinfo.value) == "Missing 'name' key(s) at 'request' scope"

    class TestHTTPMethod:
        def test_when_request_has_method(self):
            request = RequestNode(
                {"method": "put", "name": "foo", "path": "http:foo.com"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            assert request.http_method == "PUT"

        def test_when_request_has_no_method(self):
            request = RequestNode(
                {"name": "foo", "path": "http:foo.com"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            assert request.http_method == "GET"

        def test_when_method_is_invalid(self):
            request = RequestNode(
                {"method": "xxx", "name": "foo", "path": "http:foo.com"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            with pytest.raises(HTTPMethodNotAllowedError) as excinfo:
                request.http_method

            assert (
                str(excinfo.value) == "HTTP method not supported: XXX. "
                "Supported methods: ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')."
            )

    class TestName:
        def test_when_request_has_name(self):
            request = RequestNode(
                {"name": "list-users", "path": "http:foo.com"},
                endpoint=EndpointNode({"name": "foo", "requests": []}),
            )
            assert request.name == "list-users"

        @pytest.mark.skip("it should validate mandatory `name` key before")
        def test_when_request_has_no_name(self):
            with pytest.raises(MissingMandatoryKeyError) as excinfo:
                request = RequestNode(
                    {}, endpoint=EndpointNode({"name": "foo", "requests": []})
                )

            assert str(excinfo.value) == "Missing name, path at 'request'"

    class TestFullPathUrl:
        def test_when_endpoint_has_no_url(self):
            path = "http://foo.com"
            request = RequestNode(
                {"name": "foo", "path": path},
                endpoint=EndpointNode({"name": "foo", "requests": [{}], "path": ""}),
            )
            assert request.full_url_path == path

        def test_when_endpoint_has_url(self):
            endpoint_path = "http://foo.com/api"
            endpoint = EndpointNode(
                {"name": "foo", "requests": [{}], "path": endpoint_path}
            )
            request = RequestNode({"path": "/foo", "name": "foo"}, endpoint=endpoint)
            assert request.full_url_path == f"http://foo.com/api/foo"

        def test_with_trailing_slashes(self):
            endpoint = EndpointNode(
                {"name": "foo", "requests": [{}], "path": "http://foo.com/"}
            )
            request = RequestNode({"name": "foo", "path": "/foo/"}, endpoint=endpoint)
            assert request.full_url_path == "http://foo.com/foo/"

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode(
                {"name": "foo", "requests": [{}], "path": "http://foo.com/"}
            )
            request = RequestNode({"path": "/foo/", "name": "foo"}, endpoint=endpoint)
            request.full_url_path
            calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

            mock_evaluate.assert_has_calls(calls)

    class TestHeaders:
        def test_when_endpoint_has_no_headers(self):
            headers = {"abc": "def"}
            request = RequestNode(
                {"headers": headers, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            assert request.headers == headers

        def test_when_endpoint_has_headers(self):
            headers = {"abc": "def"}
            endpoint_headers = {"xxx": "www"}
            request = RequestNode(
                {"headers": headers, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode(
                    {"headers": endpoint_headers, "name": "foo", "requests": [{}]}
                ),
            )
            assert request.headers == {"abc": "def", "xxx": "www"}

        def test_with_repeated_keys(self):
            headers = {"abc": "def"}
            endpoint_headers = {"xxx": "www", "abc": "zxc"}
            request = RequestNode(
                {"headers": headers, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode(
                    {"headers": endpoint_headers, "name": "foo", "requests": [{}]}
                ),
            )
            assert request.headers == {"abc": "def", "xxx": "www"}

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode(
                {"headers": {"abc": "def"}, "name": "foo", "requests": [{}]}
            )

            request = RequestNode(
                {"headers": {"ghi": "jkl"}, "path": "http://foo.com", "name": "foo"},
                endpoint=endpoint,
            )
            request.headers
            calls = [mocker.call({"abc": "def", "ghi": "jkl"})]

            mock_evaluate.assert_has_calls(calls)

    class TestParams:
        def test_when_endpoint_has_no_params(self):
            params = {"abc": "def"}
            request = RequestNode(
                {"params": params, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            assert request.params == params

        def test_when_endpoint_has_params(self):
            params = {"abc": "def"}
            endpoint_params = {"xxx": "www"}
            request = RequestNode(
                {"params": params, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode(
                    {"params": endpoint_params, "name": "foo", "requests": [{}]}
                ),
            )
            assert request.params == {"abc": "def", "xxx": "www"}

        def test_with_repeated_keys(self):
            params = {"abc": "def"}
            endpoint_params = {"xxx": "www", "abc": "zxc"}
            request = RequestNode(
                {"params": params, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode(
                    {"params": endpoint_params, "name": "foo", "requests": [{}]}
                ),
            )
            assert request.params == {"abc": "def", "xxx": "www"}

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode(
                {"params": {"abc": "def"}, "name": "foo", "requests": [{}]}
            )

            request = RequestNode(
                {"params": {"ghi": "jkl"}, "path": "http://foo.com", "name": "foo"},
                endpoint=endpoint,
            )
            request.params
            calls = [mocker.call({"abc": "def", "ghi": "jkl"})]

            mock_evaluate.assert_has_calls(calls)

    class TestBody:
        def test_when_request_has_no_body(self):
            request = RequestNode(
                {"path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            assert request.body == {}

        def test_when_request_has_no_body(self):
            request = RequestNode(
                {"body": {"abc": "def"}, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            assert request.body == {"abc": "def"}

        def test_calls_evaluate(self, mocker, mock_evaluate):
            request = RequestNode(
                {"body": {"ghi": "jkl"}, "path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            request.body
            calls = [mocker.call({"ghi": "jkl"})]

            mock_evaluate.assert_has_calls(calls)

    class TestRun:
        @pytest.fixture
        def mock_request(self, mocker):
            return mocker.patch("scanapi.tree.request_node.requests.request")

        @pytest.fixture
        def mock_run_tests(self, mocker):
            return mocker.patch("scanapi.tree.request_node.RequestNode._run_tests")

        def test_calls_request(self, mock_request):
            request = RequestNode(
                {"path": "http://foo.com", "name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )
            result = request.run()

            mock_request.assert_called_once_with(
                request.http_method,
                request.full_url_path,
                headers=request.headers,
                params=request.params,
                json=request.body,
                allow_redirects=False,
            )

            assert result == {
                "response": mock_request(),
                "tests_results": [],
                "no_failure": True,
            }

        test_data = [
            ([{"status": "passed"}, {"status": "failed"}], False,),
            ([{"status": "passed"}, {"status": "passed"}], True,),
        ]

        @pytest.mark.parametrize("test_results, expected_no_failure", test_data)
        def test_build_result(
            self, test_results, expected_no_failure, mock_request, mock_run_tests
        ):
            mock_run_tests.return_value = test_results
            request = RequestNode(
                {"name": "foo"},
                endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
            )

            result = request.run()

            assert result == {
                "response": mock_request(),
                "tests_results": test_results,
                "no_failure": expected_no_failure,
            }

    class TestValidate:
        @pytest.fixture()
        def mock_validate_keys(self, mocker):
            return mocker.patch("scanapi.tree.request_node.validate_keys")

        def test_should_call_validate_keys(self, mock_validate_keys):
            spec = {"headers": {"foo": "bar"}, "name": "foo", "path": "foo.bar"}
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
                    "vars",
                ),
                ("name",),
                "request",
            )
            assert len(keys) == 3
            assert "headers" in keys
            assert "name" in keys
            assert "path" in keys

from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("run")
class TestRun:
    @fixture
    def mock_session_with_retry(self, mocker):
        return mocker.patch("scanapi.tree.request_node.session_with_retry")

    @fixture
    def mock_run_tests(self, mocker):
        return mocker.patch("scanapi.tree.request_node.RequestNode._run_tests")

    @fixture
    def mock_time_sleep(self, mocker):
        return mocker.patch("scanapi.tree.request_node.time.sleep")

    @fixture
    def mock_console_write_result(self, mocker):
        return mocker.patch("scanapi.tree.request_node.write_result")

    @mark.skip("should call session_with_retry with retry and verify")
    def test_call_session_with_retry(self):
        # TODO
        pass

    @mark.it("should call the request method")
    def test_calls_request(self, mock_session_with_retry, mock_time_sleep):
        request = RequestNode(
            {
                "path": "http://foo.com",
                "name": "request_name",
                "options": {"timeout": 2.3},
            },
            endpoint=EndpointNode(
                {
                    "name": "endpoint_name",
                    "requests": [{}],
                    "delay": 1,
                    "options": {"verify": False},
                }
            ),
        )
        result = request.run()

        mock_time_sleep.assert_called_once_with(0.001)

        mock_session_with_retry().__enter__().request.assert_called_once_with(
            request.http_method,
            request.full_url_path,
            headers=request.headers,
            params=request.params,
            json=request.body,
            follow_redirects=False,
            timeout=2.3,
        )

        assert result == {
            "response": mock_session_with_retry().__enter__().request(),
            "tests_results": [],
            "no_failure": True,
            "request_node_name": "request_name",
            "options": {"timeout": 2.3, "verify": False},
        }

    @mark.context("when has no `Content-Type` header")
    @mark.it("should use `json` parameter to send body")
    def test_content_type_is_not_defined(self, mock_session_with_retry):
        request = RequestNode(
            {
                "path": "http://foo.com",
                "name": "request_name",
            },
            endpoint=EndpointNode(
                {
                    "name": "endpoint_name",
                    "requests": [{}],
                }
            ),
        )

        request.run()

        mock_session_with_retry().__enter__().request.assert_called_once_with(
            request.http_method,
            request.full_url_path,
            headers=request.headers,
            params=request.params,
            json=request.body,
            follow_redirects=False,
        )

    @mark.context("when `Content-Type` header is `application/json`")
    @mark.it("should use `json` parameter to send body")
    def test_content_type_is_application_json(self, mock_session_with_retry):
        request = RequestNode(
            {
                "path": "http://foo.com",
                "name": "request_name",
                "headers": {
                    "content-type": "application/json",
                    "x-foo": "bar",
                    "x-request-id": "123",
                    "authorization": "bearer token",
                },
            },
            endpoint=EndpointNode(
                {
                    "name": "endpoint_name",
                    "requests": [{}],
                }
            ),
        )

        request.run()

        mock_session_with_retry().__enter__().request.assert_called_once_with(
            request.http_method,
            request.full_url_path,
            headers=request.headers,
            params=request.params,
            json=request.body,
            follow_redirects=False,
        )

    test_content_types = [
        "multipart/form-data",
        "application/x-www-form-urlencoded",
        "application/xml",
        "text/yaml",
        "text/plain",
        "foo",
        "foo/bar",
    ]

    @mark.parametrize("content_type", test_content_types)
    @mark.context("when `Content-Type` header isn't `application/json`")
    @mark.it("should use `data` parameter to send `body`")
    def test_content_type_is_not_application_json(
        self, mock_session_with_retry, content_type
    ):
        request = RequestNode(
            {
                "path": "http://foo.com",
                "name": "request_name",
                "headers": {"content-type": content_type},
            },
            endpoint=EndpointNode(
                {
                    "name": "endpoint_name",
                    "requests": [{}],
                }
            ),
        )

        request.run()

        mock_session_with_retry().__enter__().request.assert_called_once_with(
            request.http_method,
            request.full_url_path,
            headers=request.headers,
            params=request.params,
            data=request.body,
            follow_redirects=False,
        )

    @mark.context("when no_report is False")
    @mark.it("should call the write_result method")
    def test_calls_write_result(
        self,
        mocker,
        mock_console_write_result,
        mock_session_with_retry,
        mock_time_sleep,
    ):
        mocker.patch(
            "scanapi.tree.request_node.settings",
            {
                "no_report": False,
            },
        )

        request = RequestNode(
            {"path": "http://foo.com", "name": "request_name"},
            endpoint=EndpointNode(
                {"name": "endpoint_name", "requests": [{}], "delay": 1}
            ),
        )
        request.run()

        assert mock_console_write_result.call_count == 1

    @mark.context("when no_report is True")
    @mark.it("should not call the write_result method")
    def test_doesnt_write_result(
        self,
        mocker,
        mock_console_write_result,
        mock_session_with_retry,
        mock_time_sleep,
    ):
        mocker.patch(
            "scanapi.tree.request_node.settings",
            {
                "no_report": True,
            },
        )

        request = RequestNode(
            {"path": "http://foo.com", "name": "request_name"},
            endpoint=EndpointNode(
                {"name": "endpoint_name", "requests": [{}], "delay": 1}
            ),
        )
        request.run()

        assert not mock_console_write_result.called

    test_data = [
        (
            [{"status": "passed"}, {"status": "failed"}],
            False,
        ),
        (
            [{"status": "passed"}, {"status": "passed"}],
            True,
        ),
    ]

    @mark.parametrize("test_results, expected_no_failure", test_data)
    @mark.it("should build the result object")
    def test_build_result(
        self,
        test_results,
        expected_no_failure,
        mock_session_with_retry,
        mock_run_tests,
        mock_console_write_result,
    ):
        mock_run_tests.return_value = test_results
        request = RequestNode(
            {"name": "request_name"},
            endpoint=EndpointNode({"name": "endpoint_name", "requests": [{}]}),
        )

        result = request.run()

        assert result == {
            "response": mock_session_with_retry().__enter__().request(),
            "tests_results": test_results,
            "no_failure": expected_no_failure,
            "request_node_name": "request_name",
            "options": {},
        }

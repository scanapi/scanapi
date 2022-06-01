from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode


@mark.describe("request node")
@mark.describe("run")
class TestRun:
    @fixture
    def mock_session(self, mocker):
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

    @mark.it("should call the request method")
    def test_calls_request(self, mock_session, mock_time_sleep):
        request = RequestNode(
            {"path": "http://foo.com", "name": "request_name"},
            endpoint=EndpointNode(
                {"name": "endpoint_name", "requests": [{}], "delay": 1}
            ),
        )
        result = request.run()

        mock_time_sleep.assert_called_once_with(0.001)

        mock_session().request.assert_called_once_with(
            request.http_method,
            request.full_url_path,
            headers=request.headers,
            params=request.params,
            json=request.body,
            allow_redirects=False,
        )

        assert result == {
            "response": mock_session().request(),
            "tests_results": [],
            "no_failure": True,
            "request_node_name": "request_name",
        }

    @mark.context("when no_report is False")
    @mark.it("should call the write_result method")
    def test_calls_write_result(self, mocker, mock_console_write_result):
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
    def test_doesnt_write_result(self, mocker, mock_console_write_result):
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
        mock_session,
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
            "response": mock_session().request(),
            "tests_results": test_results,
            "no_failure": expected_no_failure,
            "request_node_name": "request_name",
        }

import errno
import logging
import os

import requests
import yaml
from pytest import fixture, mark, raises

from scanapi.errors import EmptyConfigFileError, InvalidKeyError
from scanapi.scan import scan

log = logging.getLogger(__name__)


def file_not_found(*args, **kwargs):
    raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), "invalid_path/scanapi.yaml"
    )


def empty_config_file(*args, **kwargs):
    raise EmptyConfigFileError("valid_path/scanapi.yaml")


def yaml_error(*args, **kwargs):
    raise yaml.YAMLError("error foo")


def invalid_key(*args, **kwargs):
    raise InvalidKeyError("foo", "endpoint", ["bar", "other"])


@fixture
def response(requests_mock):
    requests_mock.get("http://test.com", text="data")
    return requests.get("http://test.com")


@mark.describe("scan")
@mark.describe("scan")
class TestScan:
    @mark.context("when could not find an api spec file")
    @mark.it("should log an error")
    def test_should_log_error(self, mocker, caplog):
        mocker.patch(
            "scanapi.scan.settings",
            {
                "spec_path": "invalid_path/scanapi.yaml",
                "no_report": False,
                "open_browser": False,
            },
        )
        mocker.patch(
            "scanapi.scan.load_config_file", side_effect=file_not_found
        )
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                scan()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 4

        assert (
            "Could not find API spec file: invalid_path/scanapi.yaml. [Errno 2] No such file "
            "or directory: 'invalid_path/scanapi.yaml" in caplog.text
        )

    @mark.context("when the api spec file is empty")
    @mark.it("should an log error")
    def test_should_log_error_2(self, mocker, caplog):
        mocker.patch(
            "scanapi.scan.load_config_file", side_effect=empty_config_file
        )

        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                scan()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 4

            assert (
                "API spec file is empty. File 'valid_path/scanapi.yaml' is empty."
                in caplog.text
            )

    @mark.context("when the api spec file has an error")
    @mark.it("should log an error")
    def test_should_log_error_3(self, mocker, caplog):
        mocker.patch("scanapi.scan.load_config_file", side_effect=yaml_error)
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                scan()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 4

        assert (
            "Error loading specification file.\nPyYAML: error foo"
            in caplog.text
        )

    @mark.context("when the api spec file has an invalid key")
    @mark.it("should log an error")
    def test_should_log_error_4(self, mocker, caplog):
        mock_load_config_file = mocker.patch("scanapi.scan.load_config_file")
        mock_load_config_file.return_value = {"blah": "blah"}
        mocker.patch(
            "scanapi.scan.EndpointNode.__init__", side_effect=invalid_key
        )
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                scan()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 4

        assert (
            "Error loading API spec. Invalid key 'foo' at 'endpoint' scope. Available keys "
            "are: ['bar', 'other']" in caplog.text
        )

    @mark.context("when the api spec is ok")
    @mark.it(
        "should call reporter.write, call console.write_summary and exit the session"
    )
    def test_should_call_reporter_write_call_console_write_summary_and_exit(
        self, mocker, response
    ):
        mocker.patch(
            "scanapi.scan.settings",
            {
                "spec_path": "",
                "no_report": False,
                "open_browser": False,
                "output_path": "",
                "template": None,
            },
        )

        mock_load_config_file = mocker.patch("scanapi.scan.load_config_file")
        mock_load_config_file.return_value = {"endpoints": []}
        mock_endpoint_init = mocker.patch("scanapi.scan.EndpointNode.__init__")
        mock_endpoint_init.return_value = None
        mock_endpoint_run = mocker.patch("scanapi.scan.EndpointNode.run")
        mock_endpoint_run.return_value = [response]
        mock_reporter_write = mocker.patch("scanapi.scan.Reporter.write")
        mock_console_write_summary = mocker.patch("scanapi.scan.write_summary")

        with raises(SystemExit) as excinfo:
            scan()

        mock_reporter_write.assert_called_once_with([response], False)
        mock_console_write_summary.assert_called_once_with()

        assert excinfo.type == SystemExit
        assert excinfo.value.code == 0

    @mark.context("when the api spec is ok")
    @mark.context("when no_report is True")
    @mark.it(
        "should call console.write_results, call console.write_summary and exit the session"
    )
    def test_should_call_console_write_results_call_console_write_summary_and_exit(
        self, mocker, response
    ):
        mocker.patch(
            "scanapi.scan.settings",
            {
                "spec_path": "",
                "no_report": True,
                "open_browser": False,
                "output_path": "",
                "template": None,
            },
        )

        mock_load_config_file = mocker.patch("scanapi.scan.load_config_file")
        mock_load_config_file.return_value = {"endpoints": []}
        mock_endpoint_init = mocker.patch("scanapi.scan.EndpointNode.__init__")
        mock_endpoint_init.return_value = None
        mock_endpoint_run = mocker.patch("scanapi.scan.EndpointNode.run")
        mock_endpoint_run.return_value = [response]
        mock_console_write_results = mocker.patch("scanapi.scan.write_results")
        mock_console_write_summary = mocker.patch("scanapi.scan.write_summary")

        with raises(SystemExit) as excinfo:
            scan()

        mock_console_write_results.assert_called_once_with([response])
        mock_console_write_summary.assert_called_once_with()

        assert excinfo.type == SystemExit
        assert excinfo.value.code == 0

    @mark.context("when the api spec is ok")
    @mark.context("when open_browser is True")
    @mark.it(
        "should call reporter.write passing open_browser as True, call console.write_summary and exit the session"
    )
    def test_should_call_reporter_write_with_open_browser_true_call_console_write_summary_and_exit(
        self, mocker, response
    ):
        mocker.patch(
            "scanapi.scan.settings",
            {
                "spec_path": "",
                "no_report": False,
                "open_browser": True,
                "output_path": "",
                "template": None,
            },
        )

        mock_load_config_file = mocker.patch("scanapi.scan.load_config_file")
        mock_load_config_file.return_value = {"endpoints": []}
        mock_endpoint_init = mocker.patch("scanapi.scan.EndpointNode.__init__")
        mock_endpoint_init.return_value = None
        mock_endpoint_run = mocker.patch("scanapi.scan.EndpointNode.run")
        mock_endpoint_run.return_value = [response]
        mock_reporter_write = mocker.patch("scanapi.scan.Reporter.write")
        mock_console_write_summary = mocker.patch("scanapi.scan.write_summary")

        with raises(SystemExit) as excinfo:
            scan()

        mock_reporter_write.assert_called_once_with([response], True)
        mock_console_write_summary.assert_called_once_with()

        assert excinfo.type == SystemExit
        assert excinfo.value.code == 0

import errno
import logging
import os

import pytest
import requests
import yaml

from scanapi.errors import EmptyConfigFileError, InvalidKeyError
from scanapi.scan import scan, write_report

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


@pytest.fixture
def response(requests_mock):
    requests_mock.get("http://test.com", text="data")
    return requests.get("http://test.com")


class TestScan:
    class TestWhenCouldNotFindAPISpecFile:
        def test_should_log_error(self, mocker, caplog):
            mocker.patch(
                "scanapi.scan.settings", {"spec_path": "invalid_path/scanapi.yaml"}
            )
            mocker.patch("scanapi.scan.load_config_file", side_effect=file_not_found)
            with caplog.at_level(logging.ERROR):
                with pytest.raises(SystemExit) as excinfo:
                    scan()

                assert excinfo.type == SystemExit
                assert excinfo.value.code == 4

            assert (
                "Could not find API spec file: invalid_path/scanapi.yaml. [Errno 2] No such file "
                "or directory: 'invalid_path/scanapi.yaml" in caplog.text
            )

    class TestWhenAPISpecFileIsEmpty:
        def test_should_log_error(self, mocker, caplog):
            mocker.patch(
                "scanapi.scan.settings",
                {"spec_path": "invalid_path/scanapi.yaml", "no_report": False},
            )
            mocker.patch("scanapi.scan.load_config_file", side_effect=empty_config_file)

            with caplog.at_level(logging.ERROR):
                with pytest.raises(SystemExit) as excinfo:
                    scan()

                assert excinfo.type == SystemExit
                assert excinfo.value.code == 4

            assert (
                "API spec file is empty. File 'valid_path/scanapi.yaml' is empty."
                in caplog.text
            )

    class TestWhenAPISpecFileHasAnError:
        def test_should_log_error(self, mocker, caplog):
            mocker.patch(
                "scanapi.scan.settings",
                {"spec_path": "invalid_path/scanapi.yaml", "no_report": False},
            )
            mocker.patch("scanapi.scan.load_config_file", side_effect=yaml_error)
            with caplog.at_level(logging.ERROR):
                with pytest.raises(SystemExit) as excinfo:
                    scan()

                assert excinfo.type == SystemExit
                assert excinfo.value.code == 4

            assert "Error loading specification file.\nPyYAML: error foo" in caplog.text

    class TestWhenAPISpecHasAnInvalidKey:
        def test_should_log_error(self, mocker, caplog):
            mocker.patch(
                "scanapi.scan.settings",
                {"spec_path": "invalid_path/scanapi.yaml", "no_report": False},
            )
            mock_load_config_file = mocker.patch("scanapi.scan.load_config_file")
            mock_load_config_file.return_value = {"blah": "blah"}
            mocker.patch("scanapi.scan.EndpointNode.__init__", side_effect=invalid_key)
            with caplog.at_level(logging.ERROR):
                with pytest.raises(SystemExit) as excinfo:
                    scan()

                assert excinfo.type == SystemExit
                assert excinfo.value.code == 4

            assert (
                "Error loading API spec. Invalid key 'foo' at 'endpoint' scope. Available keys "
                "are: ['bar', 'other']" in caplog.text
            )

    class TestWhenAPISpecIsOk:
        def test_should_call_reporter(self, mocker, response):
            mocker.patch(
                "scanapi.scan.settings",
                {"spec_path": "invalid_path/scanapi.yaml", "no_report": False},
            )
            mock_load_config_file = mocker.patch("scanapi.scan.load_config_file")
            mock_load_config_file.return_value = {"endpoints": []}
            mock_endpoint_init = mocker.patch("scanapi.scan.EndpointNode.__init__")
            mock_endpoint_init.return_value = None
            mock_endpoint_run = mocker.patch("scanapi.scan.EndpointNode.run")
            mock_endpoint_run.return_value = [response]
            mock_write_report = mocker.patch("scanapi.scan.write_report")

            with pytest.raises(SystemExit) as excinfo:
                scan()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 0

            mock_endpoint_init.assert_called_once_with({"endpoints": []})
            assert mock_endpoint_run.called
            mock_write_report.assert_called_once_with([response])


class TestWriteReporter:
    def test_should_call_wr(self, mocker, response):
        mock_write = mocker.patch("scanapi.scan.Reporter.write")
        mock_reporter_init = mocker.patch("scanapi.scan.Reporter.__init__")
        mock_reporter_init.return_value = None
        mocker.patch(
            "scanapi.scan.settings",
            {
                "output_path": "out/my-report.md",
                "no_report": False,
                "reporter": "markdown",
                "template": "my-template.jinja",
            },
        )

        write_report([response])

        mock_reporter_init.assert_called_once_with(
            "out/my-report.md", "my-template.jinja"
        )
        mock_write.assert_called_once_with([response])

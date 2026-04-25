import logging

import yaml
from click.testing import CliRunner
from pytest import mark

from scanapi.cli import configure_logging, main, run

log = logging.getLogger(__name__)
runner = CliRunner()


def yaml_error(*args, **kwargs):
    raise yaml.YAMLError("error foo")


@mark.describe("cli")
@mark.describe("run")
class TestRun:
    @mark.context("when nothing wrong happens")
    @mark.it("should call save preferences")
    def test_call_save_preferences(self, mocker):
        mock_save_preferences = mocker.patch(
            "scanapi.settings.Settings.save_preferences"
        )
        result = runner.invoke(run, ["--output-path", "my_output.html"])

        assert result.exit_code == 4
        mock_save_preferences.assert_called_once_with(
            **{
                "spec_path": None,
                "output_path": "my_output.html",
                "no_report": False,
                "open_browser": False,
                "config_path": None,
                "template": None,
            }
        )

    @mark.context("when something wrong happens")
    @mark.it("should log an error")
    def test_should_log_error(self, mocker, caplog):
        mock_save_preferences = mocker.patch(
            "scanapi.settings.Settings.save_preferences",
            side_effect=yaml_error,
        )

        with caplog.at_level(logging.ERROR):
            result = runner.invoke(run, ["--output-path", "my_output.html"])

            assert mock_save_preferences.called
            assert result.exit_code == 4

        assert (
            "Error loading configuration file.\nPyYAML: error foo"
            in caplog.text
        )

    @mark.context("when nothing wrong happens")
    @mark.it("should call scan")
    def test_call_scan(self, mocker):
        mocker.patch("scanapi.settings.Settings.save_preferences")
        mock_scan = mocker.patch("scanapi.cli.scan")

        result = runner.invoke(run, ["--output-path", "my_output.html"])

        assert result.exit_code == 0
        mock_scan.assert_called_once()


@mark.describe("cli")
@mark.describe("from openapi")
class TestFromOpenAPI:
    @mark.it("should call save_preferences and openapi_to_scanapi")
    def test_from_openapi_command(self, mocker, tmp_path):
        input_path = tmp_path / "api.yaml"
        input_path.write_text("openapi: 3.0.0\n")

        mock_save_preferences = mocker.patch(
            "scanapi.settings.Settings.save_preferences"
        )
        mock_openapi_to_scanapi = mocker.patch(
            "scanapi.cli.openapi_to_scanapi"
        )

        result = runner.invoke(
            main,
            [
                "from",
                "openapi",
                str(input_path),
                "-o",
                "scanapi.yaml",
            ],
        )

        assert result.exit_code == 0
        mock_save_preferences.assert_called_once_with(
            **{
                "input_path": str(input_path),
                "base_url": None,
                "output_path": "scanapi.yaml",
                "config_path": None,
            }
        )
        mock_openapi_to_scanapi.assert_called_once()


@mark.describe("configure_logging")
class TestConfigureLogging:
    @mark.it("should configure logging when no handlers are present")
    def test_should_configure_logging(self, mocker):
        mock_logger = mocker.Mock()
        mock_logger.handlers = []
        mocker.patch("scanapi.cli.logging.getLogger", return_value=mock_logger)
        mock_rich_handler = mocker.patch(
            "scanapi.cli.RichHandler", return_value=mocker.Mock()
        )
        mock_basic_config = mocker.patch(
            "scanapi.cli.logging.basicConfig"
        )

        configure_logging("DEBUG")

        mock_basic_config.assert_called_once()
        mock_rich_handler.assert_called_once_with(
            show_time=False, markup=True, show_path=True
        )

    @mark.it("should not reconfigure logging when handlers already exist")
    def test_should_not_reconfigure_logging(self, mocker):
        mock_logger = mocker.Mock()
        mock_logger.handlers = [mocker.Mock()]
        mocker.patch("scanapi.cli.logging.getLogger", return_value=mock_logger)
        mock_basic_config = mocker.patch(
            "scanapi.cli.logging.basicConfig"
        )

        configure_logging("INFO")

        mock_basic_config.assert_not_called()

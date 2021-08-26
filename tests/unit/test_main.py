import logging

import yaml
from click.testing import CliRunner
from pytest import mark

from scanapi.__main__ import run

log = logging.getLogger(__name__)
runner = CliRunner()


def yaml_error(*args, **kwargs):
    raise yaml.YAMLError("error foo")


@mark.describe("main")
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

import logging

import yaml
from click.testing import CliRunner

from scanapi.__main__ import convert, run

log = logging.getLogger(__name__)
runner = CliRunner()


def yaml_error(*args, **kwargs):
    raise yaml.YAMLError("error foo")


class TestMain:
    class TestRun:
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
                    "config_path": None,
                    "template": None,
                }
            )

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

    class TestConvert:
        def test_should_call_openapi_to_yaml(self, mocker):
            runner = CliRunner()
            mock_openapi_to_yaml = mocker.patch(
                "scanapi.__main__.openapi_to_yaml"
            )

            result = runner.invoke(convert, "tests/data/openapi.json")
            assert result.exit_code == 0
            mock_openapi_to_yaml.assert_called_once_with(
                "tests/data/openapi.json"
            )

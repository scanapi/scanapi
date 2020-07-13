import os

from click.testing import CliRunner

from scanapi.__main__ import run, convert


class TestMain:
    class TestRun:
        def test_call_save_preferences(self, mocker):
            runner = CliRunner()
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

    class TestConvert:
        def test_should_call_openapi_to_yaml(self, mocker):
            runner = CliRunner()
            mock_openapi_to_yaml = mocker.patch("scanapi.__main__.openapi_to_yaml")

            result = runner.invoke(convert, "tests/data/openapi.json")
            assert result.exit_code == 0
            mock_openapi_to_yaml.assert_called_once_with("tests/data/openapi.json")

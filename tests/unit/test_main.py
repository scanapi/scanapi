import os

from click.testing import CliRunner

from scanapi.main import run, convert


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
            mock_openapi_to_yaml = mocker.patch("scanapi.main.openapi_to_yaml")
            result = runner.invoke(convert, '../data/openapi.json')
            os.remove('./api.yaml')

            assert result.exit_code == 0

            mock_openapi_to_yaml.assert_called_once_with('../data/openapi.json')

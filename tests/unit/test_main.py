import os
from click.testing import CliRunner

from scanapi.__main__ import run


class TestMain:
    class TestRun:
        def test_call_save_preferences(self, mocker):
            runner = CliRunner()
            mock_save_preferences = mocker.patch(
                "scanapi.settings.Settings.save_preferences"
            )
            result = runner.invoke(run, ["--output-path", "my_output.html"])

            assert result.exit_code == 0
            mock_save_preferences.assert_called_once_with(
                **{
                    "spec_path": None,
                    "output_path": "my_output.html",
                    "config_path": None,
                    "template": None,
                }
            )

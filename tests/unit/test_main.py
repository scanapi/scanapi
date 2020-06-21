from click.testing import CliRunner

from scanapi.main import main


class TestMain:
    def test_call_save_preferences(self, mocker):
        runner = CliRunner()
        mock_save_preferences = mocker.patch(
            "scanapi.settings.Settings.save_preferences"
        )
        result = runner.invoke(main, ["--output-path", "my_output.html"])

        assert result.exit_code == 4
        mock_save_preferences.assert_called_once_with(
            **{
                "spec_path": None,
                "output_path": "my_output.html",
                "config_path": None,
                "template": None,
            }
        )

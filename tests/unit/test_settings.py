import pytest
import os

from scanapi.settings import settings, DEFAULT_CONFIG_PATH


class TestSettings:
    class TestInit:
        def test_should_init_with_default_values(self):
            assert settings["spec_path"] == "api.yaml"
            assert settings["output_path"] is None
            assert settings["template"] is None

    class TestSavePreferences:
        @pytest.fixture
        def mock_save_click_preferences(self, mocker):
            return mocker.patch("scanapi.settings.Settings.save_click_preferences")

        @pytest.fixture
        def mock_save_config_file_preferences(self, mocker):
            return mocker.patch(
                "scanapi.settings.Settings.save_config_file_preferences"
            )

        class TestWhenConfigPathIsInClickPreferences:
            def test_should_pass_config_path(
                self, mock_save_click_preferences, mock_save_config_file_preferences
            ):
                preferences = {"config_path": "foo.yaml"}
                settings.save_preferences(**preferences)
                mock_save_config_file_preferences.assert_called_with("foo.yaml")
                mock_save_click_preferences.assert_called_with(**preferences)

        class TestWhenConfigPathIsNotInClickPreferences:
            def test_should_pass_config_path_as_none(
                self, mock_save_click_preferences, mock_save_config_file_preferences
            ):
                preferences = {"foo": "bar"}
                settings.save_preferences(**preferences)
                mock_save_config_file_preferences.assert_called_with(None)
                mock_save_click_preferences.assert_called_with(**preferences)

    class TestSaveClickPreferences:
        def test_should_clean_and_save_preferences(self):
            settings.save_click_preferences(
                **{
                    "spec_path": "path/spec-path",
                    "reporter": None,
                    "output_path": "path/output-path",
                    "template": None,
                    "config_path": "path/config-path",
                }
            )

            assert settings == {
                "spec_path": "path/spec-path",
                "output_path": "path/output-path",
                "template": None,
                "config_path": "path/config-path",
            }

    class TestSaveConfigFilePreferences:
        @pytest.fixture(autouse=True)
        def define_settings(self):
            settings["spec_path"] = "path/spec-path.yaml"
            settings["output_path"] = "path/output-path.yaml"
            settings["template"] = None
            settings["config_path"] = "path/config-path.yaml"

        class TestWithoutCustomConfigPath:
            class TestWithDefaultConfigFile:
                def test_should_save_preferences(self):
                    with open(DEFAULT_CONFIG_PATH, "w") as out_file:
                        out_file.write("template: path/template.jinja")

                    settings.save_config_file_preferences()
                    assert settings["template"] == "path/template.jinja"

                    os.remove(DEFAULT_CONFIG_PATH)

            class TestWithoutDefaultConfigFile:
                def test_should_not_change_preferences(self):
                    settings.save_config_file_preferences()
                    assert settings["spec_path"] == "path/spec-path.yaml"

        class TestWithCustomConfigPath:
            class TestWithConfigFile:
                def test_should_save_preferences(self):
                    config_path = "my_config_file.yaml"
                    with open(config_path, "w") as out_file:
                        out_file.write("template: template.jinja")

                    settings.save_config_file_preferences(config_path)
                    assert settings["template"] == "template.jinja"

                    os.remove(config_path)

            class TestWithoutConfigFile:
                def test_should_raise_exception(self):
                    with pytest.raises(FileNotFoundError) as excinfo:
                        config_path = "invalid/my_config_file.yaml"
                        settings.save_config_file_preferences(config_path)

                    assert (
                        str(excinfo.value)
                        == "[Errno 2] No such file or directory: 'invalid/my_config_file.yaml'"
                    )

import pytest
import os

from scanapi.settings import settings, DEFAULT_CONFIG_PATH


class TestSettings:
    class TestInit:
        def test_should_init_with_default_values(self):
            assert settings["spec_path"] == "api.yaml"
            assert settings["reporter"] == "markdown"
            assert settings["output_path"] is None
            assert settings["template"] is None

    class TestSavePreferences:
        @pytest.fixture
        def mock_save_click_preferences(self, mocker):
            return mocker.patch("scanapi.settings.save_click_preferences")

        @pytest.fixture
        def mock_save_config_file_preferences(self, mocker):
            return mocker.patch("scanapi.settings.save_config_file_preferences")

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
                "reporter": "markdown",
                "output_path": "path/output-path",
                "template": None,
                "config_path": "path/config-path",
            }

    class TestSaveConfigFilePreferences:
        @pytest.fixture(autouse=True)
        def define_settings(self):
            settings["spec_path"] = "path/spec-path"
            settings["reporter"] = "markdown"
            settings["output_path"] = "path/output-path"
            settings["template"] = None
            settings["config_path"] = "path/config-path"

        class TestWithoutCustomConfigPath:
            class TestWithDefaultConfigFile:
                def test_should_save_preferences(self):
                    with open(DEFAULT_CONFIG_PATH, "w") as out_file:
                        out_file.write("reporter: html")

                    settings.save_config_file_preferences()
                    assert settings["reporter"] == "html"

                    os.remove(DEFAULT_CONFIG_PATH)

            class TestWithoutDefaultConfigFile:
                def test_should_not_change_preferences(self):
                    settings.save_config_file_preferences()
                    assert settings["reporter"] == "markdown"

        class TestWithCustomConfigPath:
            class TestWithConfigFile:
                def test_should_save_preferences(self):
                    config_path = "my_config_file.yaml"
                    with open(config_path, "w") as out_file:
                        out_file.write("reporter: html")

                    settings.save_config_file_preferences(config_path)
                    assert settings["reporter"] == "html"

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

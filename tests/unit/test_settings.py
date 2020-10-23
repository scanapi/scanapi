import pytest

from scanapi.settings import settings


@pytest.fixture
def mock_load_config_file(mocker):
    return mocker.patch("scanapi.settings.load_config_file")


@pytest.fixture
def mock_has_local_config_file(mocker):
    return mocker.patch(
        "scanapi.settings.Settings.has_local_config_file",
        mocker.PropertyMock(return_value=True),
    )


@pytest.fixture
def mock_doesnt_have_local_config_file(mocker):
    return mocker.patch(
        "scanapi.settings.Settings.has_local_config_file",
        mocker.PropertyMock(return_value=False),
    )


@pytest.fixture
def mock_has_global_config_file(mocker):
    return mocker.patch(
        "scanapi.settings.Settings.has_global_config_file",
        mocker.PropertyMock(return_value=True),
    )


class TestSettings:
    class TestInit:
        def test_should_init_with_default_values(self):
            assert settings["spec_path"] == "scanapi.yaml"
            assert settings["output_path"] is None
            assert settings["template"] is None

    class TestSaveConfigFilePreferences:
        @pytest.fixture(autouse=True)
        def define_settings(self):
            settings["spec_path"] = "path/spec-path.yaml"
            settings["output_path"] = "path/output-path.yaml"
            settings["template"] = None
            settings["config_path"] = "path/config-path.yaml"

        class TestWithConfigPath:
            class TestWithConfigFile:
                def test_should_save_preferences(self, mock_load_config_file):
                    config_path = "my_config_file.yaml"
                    settings.save_config_file_preferences(config_path)
                    assert settings["config_path"].endswith("my_config_file.yaml")
                    mock_load_config_file.assert_called_with("my_config_file.yaml")

            class TestWithoutConfigFile:
                def test_should_raise_exception(self):
                    with pytest.raises(FileNotFoundError) as excinfo:
                        config_path = "invalid/my_config_file.yaml"
                        settings.save_config_file_preferences(config_path)

                    assert (
                        str(excinfo.value)
                        == "[Errno 2] No such file or directory: 'invalid/my_config_file.yaml'"
                    )

        class TestHasLocalConfigFile:
            def test_should_save_preferences(
                self, mock_has_local_config_file, mock_load_config_file
            ):
                settings.save_config_file_preferences()
                assert settings["config_path"].endswith("./scanapi.conf")
                mock_load_config_file.assert_called_with("./scanapi.conf")

        class TestHasGlobalConfigFile:
            def test_should_save_preferences(
                self,
                mock_doesnt_have_local_config_file,
                mock_has_global_config_file,
                mock_load_config_file,
            ):
                settings.save_config_file_preferences()
                assert settings["config_path"].endswith("scanapi/scanapi.conf")
                assert mock_load_config_file.called

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
                self, mock_save_click_preferences, mock_save_config_file_preferences,
            ):
                preferences = {"config_path": "foo.yaml"}
                settings.save_preferences(**preferences)
                mock_save_config_file_preferences.assert_called_with("foo.yaml")
                mock_save_click_preferences.assert_called_with(**preferences)

        class TestWhenConfigPathIsNotInClickPreferences:
            def test_should_pass_config_path_as_none(
                self, mock_save_click_preferences, mock_save_config_file_preferences,
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
                "no_report": False,
                "config_path": "path/config-path",
            }

    class TestHasGlobalConfigFile:
        def test_returns_true(self, mocker):
            mocker.patch("scanapi.settings.os.path.isfile", return_value=True)

            assert settings.has_global_config_file is True

        def test_returns_false(self, mocker):
            mocker.patch("scanapi.settings.os.path.isfile", return_value=False)

            assert settings.has_global_config_file is False

    class TestHasLocalConfigFile:
        def test_returns_true(self, mocker):
            mocker.patch("scanapi.settings.os.path.isfile", return_value=True)

            assert settings.has_local_config_file is True

        def test_returns_false(self, mocker):
            mocker.patch("scanapi.settings.os.path.isfile", return_value=False)

            assert settings.has_local_config_file is False

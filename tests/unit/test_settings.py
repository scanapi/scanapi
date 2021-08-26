from pytest import fixture, mark, raises

from scanapi.settings import settings


@fixture
def mock_load_config_file(mocker):
    return mocker.patch("scanapi.settings.load_config_file")


@fixture
def mock_has_local_config_file(mocker):
    return mocker.patch(
        "scanapi.settings.Settings.has_local_config_file",
        mocker.PropertyMock(return_value=True),
    )


@fixture
def mock_doesnt_have_local_config_file(mocker):
    return mocker.patch(
        "scanapi.settings.Settings.has_local_config_file",
        mocker.PropertyMock(return_value=False),
    )


@fixture
def mock_has_global_config_file(mocker):
    return mocker.patch(
        "scanapi.settings.Settings.has_global_config_file",
        mocker.PropertyMock(return_value=True),
    )


@mark.describe("settings")
@mark.describe("__init__")
class TestInit:
    @mark.it("should init with default values")
    def test_should_init_with_default_values(self):
        assert settings["spec_path"] == "scanapi.yaml"
        assert settings["output_path"] is None
        assert settings["template"] is None


@mark.describe("settings")
@mark.describe("save_config_file_preferences")
class TestSaveConfigFilePreferences:
    @fixture(autouse=True)
    def define_settings(self):
        settings["spec_path"] = "path/spec-path.yaml"
        settings["output_path"] = "path/output-path.yaml"
        settings["template"] = None
        settings["config_path"] = "path/config-path.yaml"

    @mark.context("with config path")
    @mark.context("with config file")
    @mark.it("should save preferences")
    def test_should_save_preferences(self, mock_load_config_file):
        config_path = "my_config_file.yaml"
        settings.save_config_file_preferences(config_path)
        assert settings["config_path"].endswith("my_config_file.yaml")
        mock_load_config_file.assert_called_with("my_config_file.yaml")

    @mark.context("with config path")
    @mark.context("without config file")
    @mark.it("should raise an exception")
    def test_should_raise_exception(self):
        with raises(FileNotFoundError) as excinfo:
            config_path = "invalid/my_config_file.yaml"
            settings.save_config_file_preferences(config_path)

        assert (
            str(excinfo.value)
            == "[Errno 2] No such file or directory: 'invalid/my_config_file.yaml'"
        )

    @mark.context("without config path")
    @mark.context("with a local config file")
    @mark.it("should save preferences")
    def test_should_save_preferences_2(
        self, mock_has_local_config_file, mock_load_config_file
    ):
        settings.save_config_file_preferences()
        assert settings["config_path"].endswith("./scanapi.conf")
        mock_load_config_file.assert_called_with("./scanapi.conf")

    @mark.context("without config path")
    @mark.context("with a global config file")
    @mark.it("should save preferences")
    def test_should_save_preferences_3(
        self,
        mock_doesnt_have_local_config_file,
        mock_has_global_config_file,
        mock_load_config_file,
    ):
        settings.save_config_file_preferences()
        assert settings["config_path"].endswith("scanapi/scanapi.conf")
        assert mock_load_config_file.called


@mark.describe("settings")
@mark.describe("save_preferences")
class TestSavePreferences:
    @fixture
    def mock_save_click_preferences(self, mocker):
        return mocker.patch("scanapi.settings.Settings.save_click_preferences")

    @fixture
    def mock_save_config_file_preferences(self, mocker):
        return mocker.patch(
            "scanapi.settings.Settings.save_config_file_preferences"
        )

    @mark.context("when config path is in click preferences")
    @mark.it("should pass config path")
    def test_should_pass_config_path(
        self, mock_save_click_preferences, mock_save_config_file_preferences,
    ):
        preferences = {"config_path": "foo.yaml"}
        settings.save_preferences(**preferences)
        mock_save_config_file_preferences.assert_called_with("foo.yaml")
        mock_save_click_preferences.assert_called_with(**preferences)

    @mark.context("when config path is not in click preferences")
    @mark.it("should pass config path as None")
    def test_should_pass_config_path_as_none(
        self, mock_save_click_preferences, mock_save_config_file_preferences,
    ):
        preferences = {"foo": "bar"}
        settings.save_preferences(**preferences)
        mock_save_config_file_preferences.assert_called_with(None)
        mock_save_click_preferences.assert_called_with(**preferences)


@mark.describe("settings")
@mark.describe("save_click_preferences")
class TestSaveClickPreferences:
    @mark.it("should clean and save preferences")
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
            "open_browser": False,
            "config_path": "path/config-path",
        }


@mark.describe("settings")
@mark.describe("has_global_config_file")
class TestHasGlobalConfigFile:
    @mark.context("when there is a global config file")
    @mark.it("should returns true")
    def test_returns_true(self, mocker):
        mocker.patch("scanapi.settings.os.path.isfile", return_value=True)

        assert settings.has_global_config_file is True

    @mark.context("when there is not a global config file")
    @mark.it("should returns false")
    def test_returns_false(self, mocker):
        mocker.patch("scanapi.settings.os.path.isfile", return_value=False)

        assert settings.has_global_config_file is False


@mark.describe("settings")
@mark.describe("has_local_config_file")
class TestHasLocalConfigFile:
    @mark.context("when there is a local config file")
    @mark.it("should returns true")
    def test_returns_true(self, mocker):
        mocker.patch("scanapi.settings.os.path.isfile", return_value=True)

        assert settings.has_local_config_file is True

    @mark.context("when there is not a local config file")
    @mark.it("should returns false")
    def test_returns_false(self, mocker):
        mocker.patch("scanapi.settings.os.path.isfile", return_value=False)

        assert settings.has_local_config_file is False

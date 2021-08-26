from pytest import mark, raises

from scanapi.config_loader import load_config_file
from scanapi.errors import BadConfigIncludeError, EmptyConfigFileError


@mark.describe("config loader")
@mark.describe("load_config_file")
class TestLoadConfigFile:
    @mark.context("when it is an YAML file")
    @mark.it("should load")
    def test_should_load_yaml(self):
        data = load_config_file("tests/data/scanapi.yaml")
        assert data == {
            "endpoints": [
                {
                    "name": "scanapi-demo",
                    "path": "${BASE_URL}",
                    "requests": [{"name": "health", "path": "/health/"}],
                }
            ]
        }

    @mark.context("when it is a JSON file")
    @mark.it("should load")
    def test_should_load_json(self):
        data = load_config_file("tests/data/jsonfile.json")
        assert data == {
            "endpoints": [
                {
                    "name": "scanapi-demo",
                    "path": "${BASE_URL}",
                    "requests": [{"name": "health", "path": "/health/"}],
                }
            ]
        }

    @mark.context("file does not exist")
    @mark.it("should raise an exception")
    def test_should_raise_exception(self):

        with raises(FileNotFoundError) as excinfo:
            load_config_file("invalid/path.yaml")

        assert (
            str(excinfo.value)
            == "[Errno 2] No such file or directory: 'invalid/path.yaml'"
        )

    @mark.context("file is empty")
    @mark.it("should raise an exception")
    def test_should_raise_exception_2(self):
        with raises(EmptyConfigFileError) as excinfo:
            load_config_file("tests/data/empty.yaml")

        assert str(excinfo.value) == "File 'tests/data/empty.yaml' is empty."

    @mark.context("include file does not exist")
    @mark.it("should raise an exception")
    def test_should_raise_exception_3(self):

        with raises(FileNotFoundError) as excinfo:
            load_config_file("tests/data/api_invalid_path_include.yaml")

        assert "[Errno 2] No such file or directory: " in str(excinfo.value)
        assert "tests/data/invalid_path/include.yaml'" in str(excinfo.value)

    @mark.context("include value is not a scalar")
    @mark.it("should raise an exception")
    def test_should_raise_exception_4(self):
        with raises(BadConfigIncludeError) as excinfo:
            load_config_file("tests/data/api_non_scalar_include.yaml")

        assert "Include tag value is not a scalar" in str(excinfo.value)

import pytest
import yaml

from scanapi.errors import EmptyConfigFileError, FileFormatNotSupportedError
from scanapi.config_loader import load_config_file


class TestLoadConfigFile:
    def test_should_load(self):
        data = load_config_file("tests/data/api.yaml")
        assert data == {
            "api": {
                "endpoints": [
                    {
                        "name": "scanapi-demo",
                        "path": "${BASE_URL}",
                        "requests": [{"name": "health", "path": "/health/"}],
                    }
                ]
            }
        }

    class TestLoadJson:
        def test_should_load(self):
            data = load_config_file("tests/data/jsonfile.json")
            assert data == {
                "api": {
                    "endpoints": [
                        {
                            "name": "scanapi-demo",
                            "path": "${BASE_URL}",
                            "requests": [{"name": "health", "path": "/health/"}],
                        }
                    ]
                }
            }

    class TestWhenFileDoesNotExist:
        def test_should_raise_exception(self):

            with pytest.raises(FileNotFoundError) as excinfo:
                load_config_file("invalid/path.yaml")

            assert (
                str(excinfo.value)
                == "[Errno 2] No such file or directory: 'invalid/path.yaml'"
            )

    class TestWhenFileIsEmpty:
        def test_should_raise_exception(self):
            with pytest.raises(EmptyConfigFileError) as excinfo:
                load_config_file("tests/data/empty.yaml")

            assert str(excinfo.value) == "File 'tests/data/empty.yaml' is empty."

    class TestWhenFileFormatIsNotSupported:
        def test_should_raise_exception(self):
            with pytest.raises(FileFormatNotSupportedError) as excinfo:
                load_config_file("tests/data/not_supported_format.txt")

            assert (
                str(excinfo.value)
                == "The format .txt is not supported. Supported formats: '.yaml', '.yml', '.json'. "
                "File path: 'tests/data/not_supported_format.txt'."
            )

    class TestWhenIncludeFileFormatIsNotSupported:
        def test_should_raise_exception(self):
            with pytest.raises(FileFormatNotSupportedError) as excinfo:
                load_config_file("tests/data/api_wrong_format_include.yaml")

            assert (
                str(excinfo.value)
                == "The format .txt is not supported. Supported formats: '.yaml', '.yml', '.json'. "
                "File path: 'tests/data/include.txt'."
            )

    class TestWhenIncludeFileDoesNotExist:
        def test_should_raise_exception(self):

            with pytest.raises(FileNotFoundError) as excinfo:
                load_config_file("tests/data/api_invalid_path_include.yaml")

            assert "[Errno 2] No such file or directory: " in str(excinfo.value)
            assert "tests/data/invalid_path/include.yaml'" in str(excinfo.value)

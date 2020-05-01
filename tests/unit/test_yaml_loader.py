import pytest
import yaml

from scanapi.errors import EmptySpecError
from scanapi.yaml_loader import load_yaml


class TestLoadYaml:
    def test_should_load(self):
        data = load_yaml("tests/data/api.yaml")
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
            data = load_yaml("tests/data/jsonfile.json")
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
                load_yaml("invalid/path.yaml")

            assert (
                str(excinfo.value)
                == "[Errno 2] No such file or directory: 'invalid/path.yaml'"
            )

    class TestWhenFileIsEmpty:
        def test_should_raise_exception(self):
            with pytest.raises(EmptySpecError) as excinfo:
                load_yaml("tests/data/empty.yaml")

            assert str(excinfo.value) == "API spec is empty."

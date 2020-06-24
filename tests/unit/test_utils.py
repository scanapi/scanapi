import pytest
import requests

from scanapi.errors import InvalidKeyError, MissingMandatoryKeyError
from scanapi.utils import (
    join_urls,
    validate_keys,
)
from scanapi.hide_utils import hide_sensitive_info, _hide, _override_info


@pytest.fixture
def response(requests_mock):
    requests_mock.get("http://test.com", text="data")
    return requests.get("http://test.com")


class TestJoinUrls:
    test_data = [
        (
            "http://demo.scanapi.dev/api/",
            "health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api/",
            "/health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api/",
            "/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
        ("http://demo.scanapi.dev/api", "health", "http://demo.scanapi.dev/api/health"),
        (
            "http://demo.scanapi.dev/api",
            "/health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api",
            "/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
        (
            "",
            "http://demo.scanapi.dev/api/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
        (
            "http://demo.scanapi.dev/api/health/",
            "",
            "http://demo.scanapi.dev/api/health/",
        ),
        ("", "", ""),
    ]

    @pytest.mark.parametrize("url_1, url_2, expected", test_data)
    def test_build_url_properly(self, url_1, url_2, expected):
        assert join_urls(url_1, url_2) == expected


class TestValidateKeys:
    class TestThereIsAnInvalidKey:
        def test_should_raise_an_exception(self):
            keys = ["key1", "key2"]
            available_keys = ("key1", "key3")
            mandatory_keys = ("key1", "key2")
            scope = "endpoint"

            with pytest.raises(InvalidKeyError) as excinfo:
                validate_keys(keys, available_keys, mandatory_keys, scope)

            assert (
                str(excinfo.value)
                == "Invalid key 'key2' at 'endpoint' scope. Available keys are: ('key1', 'key3')"
            )

    class TestMissingMandatoryKey:
        def test_should_raise_an_exception(self):
            keys = ["key1"]
            available_keys = ("key1", "key3")
            mandatory_keys = ("key1", "key2")
            scope = "endpoint"

            with pytest.raises(MissingMandatoryKeyError) as excinfo:
                validate_keys(keys, available_keys, mandatory_keys, scope)

            assert str(excinfo.value) == "Missing 'key2' key(s) at 'endpoint' scope"

    class TestThereIsNotAnInvalidKeysOrMissingMandotoryKeys:
        def test_should_not_raise_an_exception(self):
            keys = ["key1"]
            available_keys = ("key1", "key3")
            mandatory_keys = ("key1",)
            scope = "endpoint"

            validate_keys(keys, available_keys, mandatory_keys, scope)

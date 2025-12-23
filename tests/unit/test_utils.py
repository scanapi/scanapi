import requests
from pytest import fixture, mark, raises

from scanapi.errors import InvalidKeyError, MissingMandatoryKeyError
from scanapi.utils import join_urls, session_with_retry, validate_keys


@fixture
def response(requests_mock):
    requests_mock.get("http://test.com", text="data")
    return requests.get("http://test.com")


@mark.describe("utils")
@mark.describe("join_urls")
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
        (
            "http://demo.scanapi.dev/api",
            "health",
            "http://demo.scanapi.dev/api/health",
        ),
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

    @mark.it("should build url properly")
    @mark.parametrize("url_1, url_2, expected", test_data)
    def test_build_url_properly(self, url_1, url_2, expected):
        assert join_urls(url_1, url_2) == expected


@mark.describe("utils")
@mark.describe("validate_keys")
class TestValidateKeys:
    @mark.context("there is an invalid key")
    @mark.it("should raise an exception")
    def test_should_raise_an_exception(self):
        keys = ["key1", "key2"]
        available_keys = ("key1", "key3")
        mandatory_keys = ("key1", "key2")
        scope = "endpoint"

        with raises(InvalidKeyError) as excinfo:
            validate_keys(keys, available_keys, mandatory_keys, scope)

        assert (
            str(excinfo.value)
            == "Invalid key 'key2' at 'endpoint' scope. Available keys are: ('key1', 'key3')"
        )

    @mark.context("there is a mandatory key missing")
    @mark.it("should raise an exception")
    def test_should_raise_an_exception_2(self):
        keys = ["key1"]
        available_keys = ("key1", "key3")
        mandatory_keys = ("key1", "key2")
        scope = "endpoint"

        with raises(MissingMandatoryKeyError) as excinfo:
            validate_keys(keys, available_keys, mandatory_keys, scope)

        assert str(excinfo.value) == "Missing 'key2' key(s) at 'endpoint' scope"

    @mark.context("there is not an invalid key or a mandatory key missing")
    @mark.it("should not raise an exception")
    def test_should_not_raise_an_exception(self):
        keys = ["key1"]
        available_keys = ("key1", "key3")
        mandatory_keys = ("key1",)
        scope = "endpoint"

        validate_keys(keys, available_keys, mandatory_keys, scope)


@mark.describe("utils")
@mark.describe("session_with_retry")
class TestSessionWithRetry:
    @mark.context("there is no retry configuration")
    @mark.it("should not mount custom adapters")
    def test_should_not_mount_custom_adapters(self):
        session = session_with_retry({})

        assert session._transport._pool._retries == 0

    @mark.context("there is a retry configuration")
    @mark.it("should mount custom adapters")
    def test_should_mount_custom_adapters(self):
        session = session_with_retry({"max_retries": 7})

        assert session._transport._pool._retries == 7

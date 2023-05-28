import httpcore
import httpx
import requests
from pytest import fixture, mark, raises

from scanapi.errors import InvalidKeyError, MissingMandatoryKeyError
from scanapi.utils import join_urls, session_with_retry, validate_keys


def url_to_origin(url: str) -> httpcore.URL:
    """
    Given a URL string, return the origin in the raw tuple format that
    `httpcore` uses for it's representation.
    """
    u = httpx.URL(url)
    return httpcore.URL(
        scheme=u.raw_scheme, host=u.raw_host, port=u.port, target="/"
    )


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


PROXY_URL = "http://[::1]"


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

    @mark.parametrize(
        ["url", "proxies", "expected"],
        [
            ("http://example.com", None, None),
            ("http://example.com", {}, None),
            ("http://example.com", {"https://": PROXY_URL}, None),
            ("http://example.com", {"http://example.net": PROXY_URL}, None),
            # Using "*" should match any domain name.
            ("http://example.com", {"http://*": PROXY_URL}, PROXY_URL),
            ("https://example.com", {"http://*": PROXY_URL}, None),
            # Using "example.com" should match example.com, but not www.example.com
            (
                "http://example.com",
                {"http://example.com": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://www.example.com",
                {"http://example.com": PROXY_URL},
                None,
            ),
            # Using "*.example.com" should match www.example.com, but not example.com
            ("http://example.com", {"http://*.example.com": PROXY_URL}, None),
            (
                "http://www.example.com",
                {"http://*.example.com": PROXY_URL},
                PROXY_URL,
            ),
            # Using "*example.com" should match example.com and www.example.com
            (
                "http://example.com",
                {"http://*example.com": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://www.example.com",
                {"http://*example.com": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://wwwexample.com",
                {"http://*example.com": PROXY_URL},
                None,
            ),
            # ...
            (
                "http://example.com:443",
                {"http://example.com": PROXY_URL},
                PROXY_URL,
            ),
            ("http://example.com", {"all://": PROXY_URL}, PROXY_URL),
            (
                "http://example.com",
                {"all://": PROXY_URL, "http://example.com": None},
                None,
            ),
            ("http://example.com", {"http://": PROXY_URL}, PROXY_URL),
            (
                "http://example.com",
                {"all://example.com": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://example.com",
                {"http://example.com": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://example.com",
                {"http://example.com:80": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://example.com:8080",
                {"http://example.com:8080": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://example.com:8080",
                {"http://example.com": PROXY_URL},
                PROXY_URL,
            ),
            (
                "http://example.com",
                {
                    "all://": PROXY_URL + ":1",
                    "http://": PROXY_URL + ":2",
                    "all://example.com": PROXY_URL + ":3",
                    "http://example.com": PROXY_URL + ":4",
                },
                PROXY_URL + ":4",
            ),
            (
                "http://example.com",
                {
                    "all://": PROXY_URL + ":1",
                    "http://": PROXY_URL + ":2",
                    "all://example.com": PROXY_URL + ":3",
                },
                PROXY_URL + ":3",
            ),
            (
                "http://example.com",
                {"all://": PROXY_URL + ":1", "http://": PROXY_URL + ":2"},
                PROXY_URL + ":2",
            ),
        ],
    )
    @mark.context("there is a proxies configuration")
    @mark.it("should have proxy configured")
    def test_transport_for_request(self, url, proxies, expected):
        session = session_with_retry(proxies=proxies)
        transport = session._transport_for_url(httpx.URL(url))

        if expected is None:
            assert transport is session._transport
        else:
            assert isinstance(transport, httpx.HTTPTransport)
            assert isinstance(transport._pool, httpcore.HTTPProxy)
            assert transport._pool._proxy_url == url_to_origin(expected)

    @mark.parametrize(
        ["url", "env", "expected"],
        [
            ("http://google.com", {}, None),
            (
                "http://google.com",
                {"HTTP_PROXY": "http://example.com"},
                "http://example.com",
            ),
            # Auto prepend http scheme
            (
                "http://google.com",
                {"HTTP_PROXY": "example.com"},
                "http://example.com",
            ),
            (
                "http://google.com",
                {"HTTP_PROXY": "http://example.com", "NO_PROXY": "google.com"},
                None,
            ),
            # Everything proxied when NO_PROXY is empty/unset
            (
                "http://127.0.0.1",
                {"ALL_PROXY": "http://localhost:123", "NO_PROXY": ""},
                "http://localhost:123",
            ),
            # Not proxied if NO_PROXY matches URL.
            (
                "http://127.0.0.1",
                {"ALL_PROXY": "http://localhost:123", "NO_PROXY": "127.0.0.1"},
                None,
            ),
            # Proxied if NO_PROXY scheme does not match URL.
            (
                "http://127.0.0.1",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": "https://127.0.0.1",
                },
                "http://localhost:123",
            ),
            # Proxied if NO_PROXY scheme does not match host.
            (
                "http://127.0.0.1",
                {"ALL_PROXY": "http://localhost:123", "NO_PROXY": "1.1.1.1"},
                "http://localhost:123",
            ),
            # Not proxied if NO_PROXY matches host domain suffix.
            (
                "http://courses.mit.edu",
                {"ALL_PROXY": "http://localhost:123", "NO_PROXY": "mit.edu"},
                None,
            ),
            # Proxied even though NO_PROXY matches host domain *prefix*.
            (
                "https://mit.edu.info",
                {"ALL_PROXY": "http://localhost:123", "NO_PROXY": "mit.edu"},
                "http://localhost:123",
            ),
            # Not proxied if one item in NO_PROXY case matches host domain suffix.
            (
                "https://mit.edu.info",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": "mit.edu,edu.info",
                },
                None,
            ),
            # Not proxied if one item in NO_PROXY case matches host domain suffix.
            # May include whitespace.
            (
                "https://mit.edu.info",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": "mit.edu, edu.info",
                },
                None,
            ),
            # Proxied if no items in NO_PROXY match.
            (
                "https://mit.edu.info",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": "mit.edu,mit.info",
                },
                "http://localhost:123",
            ),
            # Proxied if NO_PROXY domain doesn't match.
            (
                "https://foo.example.com",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": "www.example.com",
                },
                "http://localhost:123",
            ),
            # Not proxied for subdomains matching NO_PROXY, with a leading ".".
            (
                "https://www.example1.com",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": ".example1.com",
                },
                None,
            ),
            # Proxied, because NO_PROXY subdomains only match if "." separated.
            (
                "https://www.example2.com",
                {
                    "ALL_PROXY": "http://localhost:123",
                    "NO_PROXY": "ample2.com",
                },
                "http://localhost:123",
            ),
            # No requests are proxied if NO_PROXY="*" is set.
            (
                "https://www.example3.com",
                {"ALL_PROXY": "http://localhost:123", "NO_PROXY": "*"},
                None,
            ),
        ],
    )
    @mark.context("there is a proxies configuration")
    @mark.it("should accept environment variables")
    def test_proxies_environ(self, monkeypatch, url, env, expected):
        for name, value in env.items():
            monkeypatch.setenv(name, value)

        session = session_with_retry()
        transport = session._transport_for_url(httpx.URL(url))

        if expected is None:
            assert transport == session._transport
        else:
            assert transport._pool._proxy_url == url_to_origin(expected)

    @mark.parametrize(
        "proxies",
        [
            {"http": "http://127.0.0.1"},
            {"https": "http://127.0.0.1"},
            {"all": "http://127.0.0.1"},
            {"foo": "bar"},
            "foo.bar",
            127,
            [1, 2, 3],
            True,
        ],
    )
    @mark.context("there is a proxies configuration")
    @mark.it("should raise an error values not accepted")
    def test_when_proxies_has_invalid(self, proxies):
        with raises((AttributeError, ValueError)):
            session_with_retry(proxies=proxies)

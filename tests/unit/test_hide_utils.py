import requests
from pytest import fixture, mark

from scanapi.hide_utils import _hide, _override_info, hide_sensitive_info


@fixture
def response(requests_mock):
    requests_mock.get("http://test.com", text="data")
    return requests.get("http://test.com")


@mark.describe("hide utils")
@mark.describe("hide_sensitive_info")
class TestHideSensitiveInfo:
    @fixture
    def mock__hide(self, mocker):
        return mocker.patch("scanapi.hide_utils._hide")

    test_data = [
        ({}, {}, {}),
        ({"report": {"abc": "def"}}, {}, {}),
        ({"report": {"hide_request": {"url": ["abc"]}}}, {"url": ["abc"]}, {}),
        (
            {"report": {"hide_request": {"headers": ["abc"]}}},
            {"headers": ["abc"]},
            {},
        ),
        (
            {"report": {"hide_response": {"headers": ["abc"]}}},
            {},
            {"headers": ["abc"]},
        ),
    ]

    @mark.it("should call _hide method")
    @mark.parametrize(
        "settings, request_settings, response_settings", test_data
    )
    def test_calls__hide(
        self,
        settings,
        request_settings,
        response_settings,
        mocker,
        response,
        mock__hide,
    ):
        mocker.patch("scanapi.hide_utils.settings", settings)
        hide_sensitive_info(response)

        calls = [
            mocker.call(response.request, request_settings),
            mocker.call(response, response_settings),
        ]

        mock__hide.assert_has_calls(calls)


@mark.describe("hide utils")
@mark.describe("_hide")
class TestHide:
    @fixture
    def mock__override_info(self, mocker):
        return mocker.patch("scanapi.hide_utils._override_info")

    test_data = [
        ({}, []),
        (
            {"headers": ["abc", "def"]},
            [("headers", "abc"), ("headers", "def")],
        ),
        ({"headers": ["abc"]}, [("headers", "abc")]),
        ({"url": ["abc"]}, []),
    ]

    @mark.it("should call _override_info method")
    @mark.parametrize("settings, calls", test_data)
    def test_calls__override_info(
        self, settings, calls, mocker, response, mock__override_info
    ):
        _hide(response, settings)
        calls = [mocker.call(response, call[0], call[1]) for call in calls]

        mock__override_info.assert_has_calls(calls)


@mark.describe("hide utils")
@mark.describe("_override_info")
class TestOverrideInfo:
    @mark.it("should overrides url")
    def test_overrides_url(self, response):
        secret_key = "129e8cb2-d19c-51ad-9921-cea329bed7fa"
        response.url = (
            "http://test.com/users/129e8cb2-d19c-51ad-9921-cea329bed7fa/details"
        )
        http_attr = "url"
        secret_field = secret_key

        _override_info(response, http_attr, secret_field)

        assert (
            response.url
            == "http://test.com/users/SENSITIVE_INFORMATION/details"
        )

    @mark.it("should overrides headers")
    def test_overrides_headers(self, response):
        response.headers = {"abc": "123"}
        http_attr = "headers"
        secret_field = "abc"

        _override_info(response, http_attr, secret_field)

        assert response.headers["abc"] == "SENSITIVE_INFORMATION"

    @mark.it("should overrides body")
    def test_overrides_body(self, response):
        response.body = (
            b'{"id": "abc21", "name": "Tarik", "yearsOfExperience": 2}'
        )
        http_attr = "body"
        secret_field = "id"

        _override_info(response, http_attr, secret_field)

        assert (
            response.body
            == b'{"id": "SENSITIVE_INFORMATION", "name": "Tarik", "yearsOfExperience": 2}'
        )

    @mark.it("should overrides content")
    def test_overrides_content(self, response):
        response._content = (
            b'{"id": "abc21", "name": "Tarik", "yearsOfExperience": 2}'
        )
        http_attr = "body"
        secret_field = "id"

        _override_info(response, http_attr, secret_field)

        assert (
            response.content
            == b'{"id": "SENSITIVE_INFORMATION", "name": "Tarik", "yearsOfExperience": 2}'
        )

    @mark.it("should overrides body and empty content")
    def test_overrides_body_and_empty_content(self, response):
        response.body = b"{}"
        response._content = b"{}"
        http_attr = "body"
        secret_field = "id"

        _override_info(response, http_attr, secret_field)

        assert response.body == b"{}"

        assert response.content == b"{}"

    @mark.it("should overrides params")
    def test_overrides_params(self, response):
        param = "test"
        response.url = (
            "http://test.com/users/details?test=test&test2=test&test=test2"
        )
        http_attr = "params"
        secret_field = param

        _override_info(response, http_attr, secret_field)

        assert (
            response.url
            == "http://test.com/users/details?test=SENSITIVE_INFORMATION&test2=test&test=SENSITIVE_INFORMATION"
        )

    @mark.context("when http attr does not have the field")
    @mark.it("should not change the http attr")
    def test_when_http_attr_does_not_have_the_field(self, response, mocker):
        response.headers = {"abc": "123"}
        http_attr = "headers"
        secret_field = "def"

        _override_info(response, http_attr, secret_field)

        assert response.headers == {"abc": "123"}

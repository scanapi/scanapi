import pytest
import requests

from scanapi.hide_utils import hide_sensitive_info, _hide, _override_info


@pytest.fixture
def response(requests_mock):
    requests_mock.get("http://test.com", text="data")
    return requests.get("http://test.com")


class TestHideSensitiveInfo:
    @pytest.fixture
    def mock__hide(self, mocker):
        return mocker.patch("scanapi.hide_utils._hide")

    test_data = [
        ({}, {}, {}),
        ({"report": {"abc": "def"}}, {}, {}),
        ({"report": {"hide-request": {"url": ["abc"]}}}, {"url": ["abc"]}, {}),
        ({"report": {"hide-request": {"headers": ["abc"]}}}, {"headers": ["abc"]}, {}),
        ({"report": {"hide-response": {"headers": ["abc"]}}}, {}, {"headers": ["abc"]}),
    ]

    @pytest.mark.parametrize("settings, request_settings, response_settings", test_data)
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


class TestHide:
    @pytest.fixture
    def mock__override_info(self, mocker):
        return mocker.patch("scanapi.hide_utils._override_info")

    test_data = [
        ({}, []),
        ({"headers": ["abc", "def"]}, [("headers", "abc"), ("headers", "def")]),
        ({"headers": ["abc"]}, [("headers", "abc")]),
        ({"url": ["abc"]}, []),
    ]

    @pytest.mark.parametrize("settings, calls", test_data)
    def test_calls__override_info(
        self, settings, calls, mocker, response, mock__override_info
    ):
        _hide(response, settings)
        calls = [mocker.call(response, call[0], call[1]) for call in calls]

        mock__override_info.assert_has_calls(calls)


class TestOverrideInfo:
    def test_overrides(self, response):
        response.headers = {"abc": "123"}
        http_attr = "headers"
        secret_field = "abc"

        _override_info(response, http_attr, secret_field)

        assert response.headers["abc"] == "SENSITIVE_INFORMATION"

    def test_overrides_sensitive_info_url(self, response):
        secret_key = "129e8cb2-d19c-51ad-9921-cea329bed7fa"
        response.url = (
            f"http://test.com/users/129e8cb2-d19c-51ad-9921-cea329bed7fa/details"
        )
        http_attr = "url"
        secret_field = secret_key

        _override_info(response, http_attr, secret_field)

        assert response.url == "http://test.com/users/SENSITIVE_INFORMATION/details"

    def test_when_http_attr_is_not_allowed(self, response, mocker):
        mocker.patch("scanapi.hide_utils.ALLOWED_ATTRS_TO_HIDE", ["body"])
        response.headers = {"abc": "123"}
        http_attr = "headers"
        secret_field = "abc"

        _override_info(response, http_attr, secret_field)

        assert response.headers["abc"] == "123"

    def test_when_http_attr_does_not_have_the_field(self, response, mocker):
        mocker.patch("scanapi.hide_utils.ALLOWED_ATTRS_TO_HIDE", ["body"])
        response.headers = {"abc": "123"}
        http_attr = "headers"
        secret_field = "def"

        _override_info(response, http_attr, secret_field)

        assert response.headers == {"abc": "123"}

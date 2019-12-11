import pytest
import requests

from scanapi.settings import SETTINGS
from tests.unit.factories import ReporterFactory


class TestReporter:
    @pytest.fixture
    def response(self, requests_mock):
        requests_mock.request(
            "get",
            "http://123-fake-api.com",
            headers={"Authorization": "abc", "Token": "123"},
        )

        return requests.request(
            "get",
            "http://123-fake-api.com",
            headers={"Authorization": "abc", "Token": "123"},
        )

    @pytest.fixture
    def req(self, response):
        return response.request

    @pytest.fixture
    def responses(self, response):
        return [response]

    @pytest.fixture
    def reporter(self):
        return ReporterFactory()

    class TestHideSensitiveInfo:
        @pytest.fixture
        def mock_hide_keys(self, mocker):
            return mocker.patch("scanapi.reporter.Reporter.hide_keys")

        @pytest.fixture
        def mock_hide_request_headers_info(self, mocker):
            return mocker.patch("scanapi.reporter.Reporter.hide_request_headers_info")

        class TestWhenThereIsNoHideKeys:
            def test_doesnt_call_hide_request_headers_info(
                self,
                reporter,
                responses,
                mock_hide_keys,
                mock_hide_request_headers_info,
            ):
                mock_hide_keys.return_value = None
                reporter.hide_headers_info(responses)
                assert not mock_hide_request_headers_info.called

        class TestWhenThereIsHideKey:
            def test_calls_hide_request_headers_info(
                self,
                reporter,
                responses,
                mock_hide_keys,
                mock_hide_request_headers_info,
            ):
                mock_hide_keys.return_value = ["Authorization"]
                reporter.hide_headers_info(responses)
                mock_hide_request_headers_info.assert_called_with(
                    responses[0].request, ["Authorization"]
                )

    class TestHideRequestHeadersInfo:
        class TestWhenThereIsNoHideSettings:
            def test_doesnt_change_the_headers(self, reporter, req):
                reporter.hide_request_headers_info(req, {})
                assert req.headers["Authorization"] == "abc"

        class TestWhenThereAreHideSettings:
            def test_changes_the_sensitive_headers(self, reporter, req):
                hide_settings = ["Authorization"]
                reporter.hide_request_headers_info(req, hide_settings)
                assert req.headers["Authorization"] == "<sensitive_information>"
                assert req.headers["Token"] == "123"

        class TestWhenThereAreMultipleHideSettings:
            def test_changes_the_sensitive_headers(self, reporter, req):
                hide_settings = ["Authorization", "Token"]
                reporter.hide_request_headers_info(req, hide_settings)
                assert req.headers["Authorization"] == "<sensitive_information>"
                assert req.headers["Token"] == "<sensitive_information>"

    class TestHideKeys:
        class TestWhenThereIsNoReportSettings:
            def test_returns_none(self, reporter):
                if SETTINGS.get("report"):
                    del SETTINGS["report"]

                assert reporter.hide_keys() is None

        class TestWhenThereReportSettingsIsEmpty:
            def test_returns_none(self, reporter):
                SETTINGS["report"] = {}

                assert reporter.hide_keys() is None

        class TestWhenThereIsNoHideSettings:
            def test_returns_none(self, reporter):
                SETTINGS["report"] = {"something": "else"}

                assert reporter.hide_keys() is None

        class TestWhenThereAreHideSettingsButNoHeaders:
            def test_returns_none(self, reporter):
                SETTINGS["report"]["hide"] = {"something": ["else"]}

                assert reporter.hide_keys() is None

        class TestWhenThereAreHideSettingsForNoHeaders:
            def test_returns_none(self, reporter):
                SETTINGS["report"]["hide"] = {"headers": ["Authorization"]}

                assert reporter.hide_keys() == ["Authorization"]

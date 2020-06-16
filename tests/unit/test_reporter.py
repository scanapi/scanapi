import pytest
import jinja2
from scanapi.reporter import Reporter

fake_responses = [
    {"status_code": 200, "request": {"method": "GET", "url": "http://test.com"}}
]


class TestReporter:
    @pytest.fixture
    def mocked__render_content(self, mocker):
        return mocker.patch("scanapi.reporter.Reporter._render_content")

    @pytest.fixture
    def mocked_open(self, mocker):
        mock = mocker.mock_open()
        mocker.patch("scanapi.reporter.open", mock)
        return mock

    def test_should_write_to_default_output(
        self, mocker, mocked__render_content, mocked_open
    ):
        mocked__render_content.return_value = "ScanAPI Report"
        reporter = Reporter()
        reporter.write(fake_responses)

        mocked_open.assert_called_once_with("scanapi-report.html", "w", newline="\n")
        mocked_open().write.assert_called_once_with("ScanAPI Report")

    def test_should_write_to_custom_output(
        self, mocker, mocked__render_content, mocked_open
    ):
        mocked__render_content.return_value = "ScanAPI Report"
        reporter = Reporter("./custom/report-output.html", "html")
        reporter.write(fake_responses)

        mocked_open.assert_called_once_with(
            "./custom/report-output.html", "w", newline="\n"
        )
        mocked_open().write.assert_called_once_with("ScanAPI Report")

    def test_should_handle_custom_templates(
        self, mocker, mocked__render_content, mocked_open
    ):
        mocked__render_content.return_value = "ScanAPI Report"
        reporter = Reporter(template="my-template.html")
        reporter.write(fake_responses)

        mocked_open.assert_called_once_with("scanapi-report.html", "w", newline="\n")
        mocked_open().write.assert_called_once_with("ScanAPI Report")

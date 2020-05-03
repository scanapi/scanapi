import pytest
import jinja2
from scanapi.reporter import Reporter

fake_responses = [
    {"status_code": 200, "request": {"method": "GET", "url": "http://test.com"}}
]


class TestConsoleReport:
    @pytest.fixture
    def mocked_print(self, mocker):
        return mocker.patch("builtins.print")

    def test_should_print(self, mocker, mocked_print):
        console_reporter = Reporter(None, "console")
        console_reporter.write(fake_responses)

        expected_content = "\n".join(
            (
                "ScanAPI Report: Console",
                "=======================",
                "",
                "GET http://test.com - 200",
                "",
            )
        )

        mocked_print.assert_called_once_with(f"\n{expected_content}")


class TestReporterOtherThanConsole:
    @pytest.fixture
    def mocked__render_content(self, mocker):
        return mocker.patch("scanapi.reporter.Reporter._render_content")

    @pytest.fixture
    def mocked_open(self, mocker):
        mock = mocker.mock_open()
        mocker.patch("builtins.open", mock)
        return mock

    @pytest.mark.parametrize("reporter_type", ["html", "markdown"])
    def test_should_write_to_default_output(
        self, reporter_type, mocker, mocked__render_content, mocked_open
    ):
        mocked__render_content.return_value = "ScanAPI Report"
        reporter = Reporter(None, reporter_type)
        reporter.write(fake_responses)

        file_extension = {"html": "html", "markdown": "md"}[reporter_type]
        mocked_open.assert_called_once_with(
            f"scanapi-report.{file_extension}", "w", newline="\n"
        )
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
        reporter = Reporter(None, None, "my-template.html")
        reporter.write(fake_responses)

        mocked_open.assert_called_once_with("scanapi-report", "w", newline="\n")
        mocked_open().write.assert_called_once_with("ScanAPI Report")

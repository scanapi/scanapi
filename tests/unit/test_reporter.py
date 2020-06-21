import pytest

from freezegun.api import FakeDatetime
from scanapi.reporter import Reporter

fake_results = [
    {"response": "foo", "tests_results": [], "no_failure": True,},
    {"response": "bar", "tests_results": [], "no_failure": False,},
]


class TestReporter:
    class TestInit:
        class TestNoArguments:
            def test_init_output_path_and_template(self):
                reporter = Reporter()

                assert reporter.output_path == "scanapi-report.html"
                assert reporter.template is None

        class TestWithTemplate:
            def test_init_output_path_and_template(self):
                reporter = Reporter(template="my_template.jinja")

                assert reporter.output_path == "scanapi-report.html"
                assert reporter.template == "my_template.jinja"

        class TestWithOutputPath:
            def test_init_output_path_and_template(self):
                reporter = Reporter(output_path="my-report.html")

                assert reporter.output_path == "my-report.html"
                assert reporter.template is None

    @pytest.mark.freeze_time("2020-05-12 11:32:34")
    class TestWrite:
        @pytest.fixture
        def mocked__render(self, mocker):
            return mocker.patch("scanapi.reporter.render")

        @pytest.fixture
        def mocked__session(self, mocker):
            return mocker.patch("scanapi.reporter.session")

        @pytest.fixture
        def context(self, mocked__session):
            return {
                "now": FakeDatetime(2020, 5, 12, 11, 32, 34),
                "project_name": "",
                "results": fake_results,
                "session": mocked__session,
            }

        @pytest.fixture
        def mocked__open(self, mocker):
            mock = mocker.mock_open()
            mocker.patch("scanapi.reporter.open", mock)
            return mock

        def test_should_write_to_default_output(
            self, mocker, mocked__render, mocked__open, mocked__session, context,
        ):
            mocked__render.return_value = "ScanAPI Report"
            reporter = Reporter()
            reporter.write(fake_results)

            mocked__render.assert_called_once_with("html.jinja", context, False)
            mocked__open.assert_called_once_with(
                "scanapi-report.html", "w", newline="\n"
            )
            mocked__open().write.assert_called_once_with("ScanAPI Report")

        def test_should_write_to_custom_output(
            self, mocker, mocked__render, mocked__open, mocked__session, context,
        ):
            mocked__render.return_value = "ScanAPI Report"
            reporter = Reporter("./custom/report-output.html", "html")
            reporter.write(fake_results)

            mocked__render.assert_called_once_with("html", context, True)
            mocked__open.assert_called_once_with(
                "./custom/report-output.html", "w", newline="\n"
            )
            mocked__open().write.assert_called_once_with("ScanAPI Report")

        def test_should_handle_custom_templates(
            self, mocker, mocked__render, mocked__open, mocked__session, context,
        ):
            mocked__render.return_value = "ScanAPI Report"
            reporter = Reporter(template="my-template.html")
            reporter.write(fake_results)

            mocked__render.assert_called_once_with("my-template.html", context, True)
            mocked__open.assert_called_once_with(
                "scanapi-report.html", "w", newline="\n"
            )
            mocked__open().write.assert_called_once_with("ScanAPI Report")

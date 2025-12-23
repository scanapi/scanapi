import pathlib

from freezegun.api import FakeDatetime
from pytest import fixture, mark

from scanapi.reporter import Reporter

fake_results = [
    {"response": "foo", "tests_results": [], "no_failure": True},
    {"response": "bar", "tests_results": [], "no_failure": False},
]


@fixture
def mock_version(mocker):
    return mocker.patch(
        "scanapi.reporter.version",
        side_effect=lambda pkg: "2.0.0" if pkg == "scanapi" else "unknown",
    )


@mark.describe("reporter")
@mark.describe("__init__")
class TestInit:
    @mark.context("when there is no argument")
    @mark.it(
        "should set output_path with the default value `scanapi-report.html`.\n\t\t\b\b"
        "should set template as None"
    )
    def test_init_output_path_and_template(self):
        reporter = Reporter()

        assert str(reporter.output_path) == "scanapi-report.html"
        assert reporter.template is None

    @mark.context("when there is a template argument")
    @mark.it(
        "should set output_path with the default value `scanapi-report.html`.\n\t\t\b\b"
        "should set template accordingly"
    )
    def test_init_output_path_and_template_2(self):
        reporter = Reporter(template="my_template.jinja")

        assert str(reporter.output_path) == "scanapi-report.html"
        assert reporter.template == "my_template.jinja"

    @mark.context("when there is an output path argument")
    @mark.it(
        "should set output_path accordingly.\n\t\t\b\bshould set template as None"
    )
    def test_init_output_path_and_template_3(self):
        reporter = Reporter(output_path="my-report.html")

        assert str(reporter.output_path) == "my-report.html"
        assert reporter.template is None


@mark.describe("reporter")
@mark.describe("write")
@mark.freeze_time("2020-05-12 11:32:34")
class TestWrite:
    @fixture
    def mocked__render(self, mocker):
        return mocker.patch("scanapi.reporter.render")

    @fixture
    def mocked__session(self, mocker):
        return mocker.patch("scanapi.reporter.session")

    @fixture
    def mocked__logger(self, mocker):
        return mocker.patch("scanapi.reporter.logger")

    @fixture
    def mocked__webbrowser(self, mocker):
        return mocker.patch("scanapi.reporter.webbrowser")

    @fixture
    def context(self, mocked__session):
        return {
            "now": FakeDatetime(2020, 5, 12, 11, 32, 34),
            "project_name": "",
            "results": fake_results,
            "session": mocked__session,
            "scanapi_version": "2.0.0",
        }

    @fixture
    def mocked__open(self, mocker):
        mock = mocker.mock_open()
        mocker.patch("scanapi.reporter.open", mock)
        return mock

    @mark.it("should write to default output")
    def test_should_write_to_default_output(
        self,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
    ):
        mocked__render.return_value = "ScanAPI Report"
        reporter = Reporter()
        reporter.write(fake_results, False)

        mocked__render.assert_called_once_with("report.html", context, False)
        mocked__open.assert_called_once_with(
            pathlib.Path("scanapi-report.html"), "w", newline="\n"
        )
        mocked__open().write.assert_called_once_with("ScanAPI Report")

    @mark.it("should write to custom output")
    def test_should_write_to_custom_output(
        self,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
    ):
        mocked__render.return_value = "ScanAPI Report"
        reporter = Reporter("./custom/report-output.html", "html")
        reporter.write(fake_results, False)

        mocked__render.assert_called_once_with("html", context, True)
        mocked__open.assert_called_once_with(
            pathlib.Path("./custom/report-output.html"), "w", newline="\n"
        )
        mocked__open().write.assert_called_once_with("ScanAPI Report")

    @mark.it("should handle custom templates")
    def test_should_handle_custom_templates(
        self,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
    ):
        mocked__render.return_value = "ScanAPI Report"
        reporter = Reporter(template="my-template.html")
        reporter.write(fake_results, False)

        mocked__render.assert_called_once_with(
            "my-template.html", context, True
        )
        mocked__open.assert_called_once_with(
            pathlib.Path("scanapi-report.html"), "w", newline="\n"
        )
        mocked__open().write.assert_called_once_with("ScanAPI Report")

    @mark.it("should open report in browser")
    def test_should_open_report_in_browser(
        self,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
        mocked__webbrowser,
    ):
        reporter = Reporter()
        reporter.write(fake_results, True)
        assert mocked__webbrowser.open.call_count == 1


@mark.describe("reporter")
@mark.describe("_build_context")
class TestBuildContext:
    @mark.it("should return context with scanapi version when package found")
    def test_build_context_with_version(self, mock_version):
        results = fake_results
        context = Reporter._build_context(results)
        assert context["scanapi_version"] == "2.0.0"
        assert context["results"] == results
        assert "now" in context
        assert "project_name" in context
        assert "session" in context

    @mark.it(
        "should return context with 'unknown' scanapi version when package not found"
    )
    def test_build_context_with_package_not_found(self, mocker):
        # Patch version to raise PackageNotFoundError
        def raise_not_found(pkg):
            from importlib.metadata import PackageNotFoundError

            raise PackageNotFoundError

        _ = mocker.patch(
            "scanapi.reporter.version", side_effect=raise_not_found
        )

        results = fake_results
        context = Reporter._build_context(results)
        assert context["scanapi_version"] == "unknown"
        assert context["results"] == results
        assert "now" in context
        assert "project_name" in context
        assert "session" in context

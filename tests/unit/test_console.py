from datetime import timedelta
from unittest.mock import MagicMock

from pytest import fixture, mark
from scanapi.console import write_report_path, write_results


@fixture
def mocked__console(mocker):
    return mocker.patch("scanapi.console.console")


@mark.describe("console")
@mark.describe("write_results")
class TestWriteResults:
    @fixture
    def mocked__session(self, mocker):
        session = MagicMock()
        session.errors = 0
        session.elapsed_time.return_value = timedelta(seconds=3)
        return mocker.patch("scanapi.console.session", session)

    @mark.context("when session has successes and no failures")
    @mark.it("should write results and write summary")
    def test_write_success(self, mocked__console, mocked__session):

        test_success = {
            "name": "should_be_success",
            "status": "passed",
            "failure": None,
            "error": None,
        }
        fake_results_passed = [
            {
                "response": "foo",
                "tests_results": [test_success],
                "no_failure": True,
            },
        ]

        mocked__session.failures = 0
        mocked__session.successes = 1

        write_results(fake_results_passed)

        mocked__console.print.assert_called_once_with(
            "[bright_green] [PASSED] [white]should_be_success"
        )

        mocked__console.rule.assert_called_once_with(
            "[bright_green]1 passed in 3.0s", characters="=",
        )

    @mark.context("when session has failures")
    @mark.it("should write results and write summary")
    def test_write_failures(self, mocker, mocked__console, mocked__session):
        tests = [
            {
                "name": "failed_test",
                "status": "failed",
                "failure": "response.status_code == 200",
                "error": None,
            },
            {
                "name": "should_be_success",
                "status": "passed",
                "failure": None,
                "error": None,
            },
        ]
        fake_results_failed = [
            {"response": "foo", "tests_results": tests, "no_failure": True,},
        ]

        mocked__session.failures = 1
        mocked__session.successes = 1

        write_results(fake_results_failed)

        calls = [
            mocker.call(
                "[bright_red] [FAILED] [white]failed_test\n\t  [bright_red]response.status_code == 200 is false"
            ),
            mocker.call("[bright_green] [PASSED] [white]should_be_success"),
        ]

        mocked__console.print.assert_has_calls(calls)

        mocked__console.rule.assert_called_once_with(
            "[bright_green]1 passed, [bright_red]1 failed, [bright_red]0 errors in 3.0s",
            characters="=",
            style="bright_red",
        )

    @mark.context("when session has no tests")
    @mark.it("should just write summary")
    def test_write_without_tests(
        self, mocker, mocked__console, mocked__session
    ):

        fake_results_failed = [
            {"response": "foo", "tests_results": [], "no_failure": True,},
        ]

        mocked__session.failures = 0
        mocked__session.successes = 0

        write_results(fake_results_failed)

        assert not mocked__console.print.called

        mocked__console.rule.assert_called_once_with(
            "[bright_green]0 passed in 3.0s", characters="=",
        )


@mark.describe("console")
@mark.describe("write_report_path")
class TestLogReport:
    @mark.it("should write report path")
    def test(self, mocked__console):

        write_report_path("http://localhost:8080")

        mocked__console.print.assert_called_once_with(
            "The documentation was generated successfully.\n"
            "It is available at -> [deep_sky_blue1 underline]http://localhost:8080\n"
        )

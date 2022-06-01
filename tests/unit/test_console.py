from datetime import timedelta
from unittest.mock import MagicMock

from pytest import fixture, mark

from scanapi.console import (
    write_report_path,
    write_result,
    write_results,
    write_summary,
)


@fixture
def mocked__console(mocker):
    return mocker.patch("scanapi.console.console")


@mark.describe("console")
@mark.describe("write_result")
class TestWriteResults:
    @fixture
    def mocked__write_result(self, mocker):
        return mocker.patch("scanapi.console.write_result")

    @mark.context("when results is empty")
    @mark.it("should not call write_result")
    def test_should_not_call(self, mocked__write_result):
        write_results([])

        assert not mocked__write_result.called

    @mark.context("when results has size 3")
    @mark.it("should call write_result 3 times")
    def test_should_call_3_times(self, mocked__write_result):
        write_results([1, 2, 3])

        assert mocked__write_result.call_count == 3


@mark.describe("console")
@mark.describe("write_result")
class TestWriteResult:
    @mark.context("when tests results contains one success")
    @mark.it("should print the success result")
    def test_write_success(self, mocked__console):

        tests_results = [
            {
                "name": "should_be_success",
                "status": "passed",
                "failure": None,
                "error": None,
            }
        ]

        fake_result_passed = {
            "tests_results": tests_results,
        }

        write_result(fake_result_passed)

        mocked__console.print.assert_called_once_with(
            "[bright_green] [PASSED] [white]should_be_success"
        )

    @mark.context("when tests results contains one success and one failure")
    @mark.it(
        "should print two lines, one for the success and one for the failure"
    )
    def test_write_failures(self, mocker, mocked__console):
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

        fake_result_failed = {
            "tests_results": tests,
        }

        write_result(fake_result_failed)

        calls = [
            mocker.call(
                "[bright_red] [FAILED] [white]failed_test\n\t  [bright_red]response.status_code == 200 is false"
            ),
            mocker.call("[bright_green] [PASSED] [white]should_be_success"),
        ]

        mocked__console.print.assert_has_calls(calls)

    @mark.context("when session has no tests")
    @mark.it("should print nothing")
    def test_write_without_tests(self, mocked__console):
        fake_result_failed = {
            "tests_results": [],
        }

        write_result(fake_result_failed)

        assert not mocked__console.print.called


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


@mark.describe("console")
@mark.describe("write_summary")
class TestWriteSummary:
    @fixture
    def mocked__session(self, mocker):
        session = MagicMock()
        session.errors = 0
        session.elapsed_time.return_value = timedelta(seconds=3)
        return mocker.patch("scanapi.console.session", session)

    @mark.context("when session has successes and no failures")
    @mark.it("should print the success summary")
    def test_write_success(self, mocked__console, mocked__session):
        mocked__session.failures = 0
        mocked__session.successes = 1

        write_summary()

        mocked__console.rule.assert_called_once_with(
            "[bright_green]1 passed in 3.0s",
            characters="=",
        )

    @mark.context("when session has failures")
    @mark.it("should print the failure summary")
    def test_write_failures(self, mocked__console, mocked__session):
        mocked__session.failures = 1
        mocked__session.successes = 1

        write_summary()

        mocked__console.rule.assert_called_once_with(
            "[bright_green]1 passed, [bright_red]1 failed, [bright_red]0 errors in 3.0s",
            characters="=",
            style="bright_red",
        )

    @mark.context("when session has no tests")
    @mark.it("should print the success summary")
    def test_write_without_tests(self, mocked__console, mocked__session):

        mocked__session.failures = 0
        mocked__session.successes = 0

        write_summary()

        mocked__console.rule.assert_called_once_with(
            "[bright_green]0 passed in 3.0s",
            characters="=",
        )

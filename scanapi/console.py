from rich.console import Console

from scanapi.session import session
from scanapi.test_status import TestStatus

console = Console()


def write_results(results):
    """Print the test results to the console output

    Returns:
        None
    """
    for r in results:
        write_result(r)


def write_result(result):
    """Print the test result to the console output

    Returns:
        None
    """
    for test in result["tests_results"]:
        if test["status"] is TestStatus.PASSED:
            console.print(f"[bright_green] [PASSED] [white]{test['name']}")
        if test["status"] == TestStatus.FAILED:
            console.print(
                f"[bright_red] [FAILED] [white]{test['name']}\n"
                f"\t  [bright_red]{test['failure']} is false"
            )


def write_report_path(uri):
    """Print path to generated documentation

    Returns:
        None
    """
    console.print(
        f"The documentation was generated successfully.\n"
        f"It is available at -> [deep_sky_blue1 underline]{uri}\n"
    )


def write_summary():
    """Write tests summary in console

    Returns:
        None
    """
    elapsed_time = round(session.elapsed_time().total_seconds(), 2)

    if session.failures > 0 or session.errors > 0:
        _print_summary_with_failures_or_errors(elapsed_time)
        return

    _print_successful_summary(elapsed_time)


def _print_summary_with_failures_or_errors(elapsed_time):
    """Write tests summary when there are failures or errors

    Returns:
        None
    """
    summary = (
        f"[bright_green]{session.successes} passed, "
        f"[bright_red]{session.failures} failed, "
        f"[bright_red]{session.errors} errors in {elapsed_time}s"
    )
    console.line()
    console.rule(summary, characters="=", style="bright_red")
    console.line()


def _print_successful_summary(elapsed_time):
    """Write tests summary when there are no failures or errors

    Returns:
        None
    """
    console.line()
    console.rule(
        f"[bright_green]{session.successes} passed in {elapsed_time}s",
        characters="=",
    )
    console.line()

from rich.console import Console

from scanapi.test_status import TestStatus
from scanapi.session import session


console = Console()


def write_results(results):
    """Print the test results to the console output

    Returns:
        None
    """
    for r in results:
        for test in r["tests_results"]:
            if test["status"] is TestStatus.PASSED:
                console.print(f"[bright_green] [PASSED] [white]{test['name']}")
            if test["status"] == TestStatus.FAILED:
                console.print(
                    f"[bright_red] [FAILED] [white]{test['name']}\n"
                    f"\t[bright_red]{test['failure']} is false"
                )
    _write_summary()


def log_report(uri):
    """Print path to generated documentation

    Returns:
        None
    """
    console.print(
        f"The documentation was generated successfully.\n"
        f"It is available at -> [deep_sky_blue1 underline]{uri}\n"
    )


def _write_summary():
    """Write tests summary in console

    Returns:
        None
    """
    elapsedTime = round(session.elapsed_time().total_seconds(), 2)
    console.line()
    if session.failures > 0 or session.errors > 0:
        summary = (
            f"[bright_green]{session.successes} passed, "
            f"[bright_red]{session.failures} failed, "
            f"[bright_red]{session.errors} errors in {elapsedTime}s"
        )
        console.rule(summary, characters="=", style="bright_red")
    else:
        console.rule(
            f"[bright_green]{session.successes} passed in {elapsedTime}s",
            characters="=",
        )
    console.line()

from rich.console import Console

from scanapi.session import session
from scanapi.test_status import TestStatus

console = Console()


def write_results(results):
    """Print the test results to the console output

    Returns:
        None: This function does not return a value. It prints directly
            to the console output.
    """
    for r in results:
        write_result(r)


def write_result(result):
    """Print the test result to the console output

    Returns:
        None: This function does not return a value. It prints directly
            to the console output.
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
        None: This function does not return a value. It prints the success
            message and the documentation link directly to the console output.
    """
    console.print(
        f"The documentation was generated successfully.\n"
        f"It is available at -> [deep_sky_blue1 underline]{uri}\n"
    )


def write_summary():
    """Write tests summary in console

    Returns:
        None: None: This function does not return a value. It prints the execution
            time and test results summary directly to the console output.
    """
    elapsed_time = round(session.elapsed_time().total_seconds(), 2)

    if session.failures > 0 or session.errors > 0:
        _print_summary_with_failures_or_errors(elapsed_time)
        return

    _print_successful_summary(elapsed_time)


def _print_summary_with_failures_or_errors(elapsed_time):
    """Write tests summary when there are failures or errors

    Returns:
        None: This function does not return a value. It prints the detailed
            failure and error counts directly to the console output.
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
        None: This function does not return a value. It prints the successful
            test results summary directly to the console output.
    """
    console.line()
    console.rule(
        f"[bright_green]{session.successes} passed in {elapsed_time}s",
        characters="=",
    )
    console.line()

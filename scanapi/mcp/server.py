from mcp.server.fastmcp import FastMCP

from scanapi.scan import run_scan  # pragma: no cover
from scanapi.settings import settings  # pragma: no cover
from scanapi.cli import configure_logging  # pragma: no cover


mcp = FastMCP("scanapi")


@mcp.tool()
def run(  # pragma: no cover
    spec_path: str,
    config_path: str | None = None,
    output_path: str | None = None,
    no_report: bool = False,
    browser: bool = False,
    template: str | None = None,
    log_level: str = "INFO",
) -> dict:
    """Run ScanAPI against an API specification.

    Args:
        spec_path (str): Path to the API specification file.
        config_path (str | None, optional): Configuration file path. Default is scanapi.conf.
        output_path (str | None, optional): Report output path. Default is scanapi-report.html.
        no_report (bool, optional): Run ScanAPI without generating a report.
        browser (bool, optional): Open the results file using a browser.
        template (str | None, optional): Custom report template path. The template must be a .jinja file.
        log_level (str, optional): Set the logging level (e.g. DEBUG, INFO).

    Returns:
        dict: A dictionary containing the summary and results of the scan.
    """
    configure_logging(log_level)

    # Save preferences to the global settings
    settings.save_preferences(
        spec_path=spec_path,
        output_path=output_path,
        no_report=no_report,
        config_path=config_path,
        template=template,
        open_browser=browser,
    )

    results = run_scan()

    # Generate report if needed
    if not no_report:
        from scanapi.scan import _write

        _write(results)

    from scanapi.session import session

    total_tests = session.successes + session.failures + session.errors

    return {
        "summary": {
            "requests": len(results),
            "tests": total_tests,
            "passed": session.successes,
            "failed": session.failures,
            "success": session.succeed,
        },
        "results": results,
    }


def main():  # pragma: no cover
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

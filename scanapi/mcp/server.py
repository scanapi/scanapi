from mcp.server.fastmcp import FastMCP

from scanapi.scan import run_scan
from scanapi.settings import settings
from scanapi.cli import configure_logging


mcp = FastMCP("scanapi")


@mcp.tool()
def run(
    spec_path: str,
    config_path: str | None = None,
    output_path: str | None = None,
    no_report: bool = False,
    browser: bool = False,
    template: str | None = None,
    log_level: str = "INFO",
) -> dict:
    """
    Run ScanAPI against an API specification.

    Args:
        spec_path: Path to the API specification file.
        config_path: Configuration file path. Default is scanapi.conf.
        output_path: Report output path. Default is scanapi-report.html.
        no_report: Run ScanAPI without generating a report.
        browser: Open the results file using a browser.
        template: Custom report template path. The template must be a .jinja file.
        log_level: Set the logging level (e.g. DEBUG, INFO).
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

    context = run_scan()

    # Generate report if needed
    if not no_report:
        from scanapi.scan import _write

        _write(context["results"])

    return {"summary": context["summary"], "results": context["results"]}


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

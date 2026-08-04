"""MCP Server for ScanAPI."""

from fastmcp import FastMCP

from scanapi.scan import run_scan  # pragma: no cover
from scanapi.settings import settings  # pragma: no cover
from scanapi.cli import configure_logging  # pragma: no cover
from scanapi.scan import write_output  # pragma: no cover
from scanapi.session import session  # pragma: no cover


mcp = FastMCP("scanapi")


@mcp.tool()
# pylint: disable=too-many-arguments,too-many-positional-arguments
# skipcq: PTC-W0049
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
        template (str | None, optional): Custom report template path.
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
        write_output(results)

    total_tests = session.successes + session.failures + session.errors

    # Serialize results to ensure they are JSON serializable for MCP transport
    serialized_results = []
    for r in results:
        response_obj = r.get("response")
        serialized_resp = None
        if response_obj:
            elapsed_obj = getattr(response_obj, "elapsed", None)
            serialized_resp = {
                "status_code": getattr(response_obj, "status_code", None),
                "url": str(getattr(response_obj, "url", "")),
                "method": getattr(getattr(response_obj, "request", None), "method", ""),
                "elapsed": elapsed_obj.total_seconds() if elapsed_obj else 0,
                "text": getattr(response_obj, "text", ""),
            }

        tests_results = []
        for t in r.get("tests_results", []):
            status = t.get("status")
            status_str = status.name if hasattr(status, "name") else str(status)
            tests_results.append({
                "name": t.get("name"),
                "status": status_str,
                "failure": t.get("failure"),
            })

        serialized_results.append({
            "request_node_name": r.get("request_node_name"),
            "endpoint_name": r.get("endpoint_name"),
            "no_failure": r.get("no_failure"),
            "response": serialized_resp,
            "tests_results": tests_results,
        })

    return {
        "summary": {
            "requests": len(results),
            "tests": total_tests,
            "passed": session.successes,
            "failed": session.failures,
            "success": session.succeed,
        },
        "results": serialized_results,
    }


def main():  # pragma: no cover
    """Start the MCP server using the stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

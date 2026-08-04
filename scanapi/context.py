import datetime
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Iterable

from scanapi.session import session
from scanapi.settings import settings


def build_context(results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Build context dict of values representing the scan execution result."""
    try:
        scanapi_version = version("scanapi")
    except PackageNotFoundError:
        scanapi_version = "unknown"

    results_list = list(results)
    total_tests = session.successes + session.failures + session.errors

    return {
        "now": datetime.datetime.now().replace(microsecond=0),
        "project_name": settings.get("project_name", ""),
        "summary": {
            "requests": len(results_list),
            "tests": total_tests,
            "passed": session.successes,
            "failed": session.failures,
            "success": session.succeed,
        },
        "results": results_list,
        "session": {
            "errors": session.errors,
            "failures": session.failures,
            "successes": session.successes,
            "exit_code": session.exit_code,
        },
        "scanapi_version": scanapi_version,
    }

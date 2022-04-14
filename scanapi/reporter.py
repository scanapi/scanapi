#!/usr/bin/env python3
import datetime
import logging
import pathlib
import webbrowser

from pkg_resources import get_distribution
from rich.console import Console

from scanapi.session import session
from scanapi.settings import settings
from scanapi.template_render import render
from scanapi.test_status import TestStatus

logger = logging.getLogger(__name__)
console = Console()


class Reporter:
    """Class that writes the scan report

    Attributes:
        output_path[str, optional]: Report output path
        template[str, optional]: Custom report template path

    """

    def __init__(self, output_path=None, template=None):
        """Creates a Reporter instance object."""
        self.output_path = pathlib.Path(output_path or "scanapi-report.html")
        self.template = template

    def write(self, results):
        """Part of the Reporter instance that is responsible for writing
        scanapi-report.html.

        Args:
            results [generator]: generator of dicts resulting of Request run().

        Returns:
            None

        """
        logger.info("\nWriting documentation")

        template_path = self.template if self.template else "report.html"
        has_external_template = bool(self.template)
        context = self._build_context(results)

        content = render(template_path, context, has_external_template)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("\nThe documentation was generated successfully.")
        console.print(
            f"It is available at [deep_sky_blue1]{self.output_path.resolve().as_uri()}"
        )

    def open_report_in_browser(self):
        """Open the results file on a browser"""
        webbrowser.open(self.output_path.resolve().as_uri())

    def write_summary_in_console(self):
        """Write the summary in console"""
        elapsedTime = round(session.elapsed_time().total_seconds(), 2)
        console.line()
        if session.failures > 0 or session.errors > 0:
            console.rule(
                f"[bright_green]{session.successes} passed, [bright_red]{session.failures} failed, [bright_red]{session.errors} errors in {elapsedTime}s",
                characters="=",
                style="bright_red",
            )
        else:
            console.rule(
                f"[bright_green]{session.successes} passed in {elapsedTime}s",
                characters="=",
            )
        console.line()

    @staticmethod
    def write_without_generating_report(results):
        """Part of the Reporter instance that is responsible for writing the
        results without generating the scanapi-report.html.

        Args:
            results [generator]: generator of dicts resulting of Request run().

        Returns:
            None
        """
        logger.info("\nWriting results without generating report")
        for r in results:
            if logger.root.level != logging.DEBUG:
                for test in r["tests_results"]:
                    if test["status"] is TestStatus.PASSED:
                        console.print(
                            f"[bright_green] [PASSED] [white]{test['name']}"
                        )
                    if test["status"] == TestStatus.FAILED:
                        console.print(
                            f"[bright_red] [FAILED] [white]{test['name']}"
                        )

    @staticmethod
    def _build_context(results):
        """Build context 2 dict of values required to render template.

        Args:
            results [generator]: generator of dicts resulting of Request run().

        Returns:
            [dict]: values required to render template.

        """
        return {
            "now": datetime.datetime.now().replace(microsecond=0),
            "project_name": settings.get("project_name", ""),
            "results": results,
            "session": session,
            "scanapi_version": get_distribution("scanapi").version,
        }

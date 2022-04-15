#!/usr/bin/env python3
import datetime
import logging
import pathlib
import webbrowser

from pkg_resources import get_distribution

from scanapi.console import console, log_report
from scanapi.session import session
from scanapi.settings import settings
from scanapi.template_render import render
from scanapi.test_status import TestStatus

logger = logging.getLogger(__name__)


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

    def write(self, results, open_in_browser):
        """Part of the Reporter instance that is responsible for writing
        scanapi-report.html.

        Args:
            results [generator]: generator of dicts resulting of Request run().

        Returns:
            None

        """
        template_path = self.template if self.template else "report.html"
        has_external_template = bool(self.template)
        context = self._build_context(results)

        content = render(template_path, context, has_external_template)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        log_report(self.output_path.resolve().as_uri())

        if open_in_browser:
            self.open_in_browser()

    def open_in_browser(self):
        """Open the results file on a browser"""
        webbrowser.open(self.output_path.resolve().as_uri())

    @staticmethod
    def write_summary_in_console():
        """Write the summary in console"""
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

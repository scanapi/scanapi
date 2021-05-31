#!/usr/bin/env python3
import datetime
import logging
from os.path import abspath

from pkg_resources import get_distribution

from scanapi.session import session
from scanapi.settings import settings
from scanapi.template_render import render

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, output_path=None, template=None):
        """ Creates a Reporter instance object. """
        self.output_path = output_path or "scanapi-report.html"
        self.template = template

    def write(self, results):
        """Part of the Reporter instance that is responsible for writing scanapi-report.html.
        Args:
            results [generator]: generator of dicts resulting of Request run().
        Returns:
            None
        """
        logger.info("Writing documentation")

        template_path = self.template if self.template else "report.html"
        has_external_template = True if self.template else False
        context = self._build_context(results)

        content = render(template_path, context, has_external_template)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("\nThe documentation was generated successfully.")
        logger.info(f"It is available at {abspath(self.output_path)}")

    @staticmethod
    def _build_context(results):
        """Build context dict of values required to render template.
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

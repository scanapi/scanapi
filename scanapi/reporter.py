#!/usr/bin/env python3
import datetime
import logging

from scanapi.session import session
from scanapi.settings import settings
from scanapi.template_render import render

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, output_path=None, template=None):
        self.output_path = output_path or "scanapi-report.html"
        self.template = template

    def write(self, results):
        logger.info("Writing documentation")

        template_path = self.template if self.template else "html.jinja"
        has_external_template = True if self.template else False
        context = self._build_context(results)

        content = render(template_path, context, has_external_template)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("\nThe documentation was generated successfully.")
        logger.info(f"It is available at {self.output_path}")

    def _build_context(self, results):
        return {
            "now": datetime.datetime.now().replace(microsecond=0),
            "project_name": settings.get("project-name", ""),
            "results": results,
            "session": session,
        }

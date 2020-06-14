#!/usr/bin/env python3
import curlify
import datetime
import logging

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from scanapi.settings import settings

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, output_path=None, template=None):
        self.output_path = output_path or "scanapi-report.html"
        self.template = template

    def write(self, responses):
        logger.info("Writing documentation")

        if self.template:
            loader = FileSystemLoader(searchpath="./")
            template_path = self.template
        else:
            loader = PackageLoader("scanapi", "templates")
            template_path = "html.jinja"

        content = self._render_content(loader, template_path, responses)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("\nThe documentation was generated successfully.")
        logger.info(f"It is available at {self.output_path}")

    def _render_content(self, loader, template_path, responses):
        env = Environment(loader=loader)
        env.filters["curlify"] = curlify.to_curl
        env.globals["now"] = datetime.datetime.now().replace(microsecond=0)
        env.globals["project_name"] = settings.get("project-name", "")
        chosen_template = env.get_template(template_path)
        return chosen_template.render(responses=responses)

#!/usr/bin/env python3
import logging
import curlify

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from scanapi.settings import settings

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, output_path, reporter, template=None):
        self.output_path = output_path
        self.reporter = reporter
        self.template = template

    def write(self, responses):
        logger.info("Writing documentation")

        if self.template:
            loader = FileSystemLoader(searchpath="./")
            template_path = self.template
        else:
            loader = PackageLoader("scanapi", "templates")
            template_path = f"{self.reporter}.jinja"

        content = self._render_content(loader, template_path, responses)

        if self.reporter == "console":
            print(f"\n{content}")
            return

        if self.output_path is None:
            outputs = {"html": "scanapi-report.html", "markdown": "scanapi-report.md"}
            self.output_path = outputs.get(self.reporter) or "scanapi-report"

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("The documentation was generated successfully.")
        logger.info(f"It is available at {self.output_path}")

    def _render_content(self, loader, template_path, responses):
        env = Environment(loader=loader)
        env.filters["curlify"] = curlify.to_curl
        chosen_template = env.get_template(template_path)
        return chosen_template.render(responses=responses)

#!/usr/bin/env python3
from jinja2 import Environment, PackageLoader, select_autoescape
import logging

from scanapi.settings import SETTINGS

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, output_path, reporter, template):
        self.output_path = output_path
        self.reporter = reporter
        self.template = template

    def write(self, responses):
        logger.info("Writing documentation")

        env = Environment(loader=PackageLoader("scanapi", "templates"))
        template = env.get_template(f"{self.reporter}.jinja")
        content = template.render(responses=responses)

        if self.reporter == "console":
            print(f"\n{content}")
            return

        if self.output_path is None:
            outputs = {"html": "scanapi-report.html", "markdown": "scanapi-report.md"}
            self.output_path = outputs.get(self.reporter)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("The documentation was generated successfully.")
        logger.info(f"It is available at {self.output_path}")

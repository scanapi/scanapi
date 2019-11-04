#!/usr/bin/env python3
from jinja2 import Environment, PackageLoader, select_autoescape
import logging

from scanapi.settings import SETTINGS

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, docs_path, reporter, template):
        self.docs_path = docs_path
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

        if self.docs_path is None:
            outputs = {"html": "docs.html", "markdown": "docs.md"}
            self.docs_path = outputs.get(self.reporter)

        with open(self.docs_path, "w", newline="\n") as doc:
            doc.write(content)

        logger.info("The documentation was generated successfully.")
        logger.info(f"It is available at {self.docs_path}")

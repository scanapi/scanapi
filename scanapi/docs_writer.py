#!/usr/bin/env python3

# TODO LIST
# criar jinja template default para Markdown
# usar jinja template para Markdown Report
# criar jinja template default para HTML
# criar HTML Report
# pensar se vale a pena trazer o hide_sensitive_informations pra dentro do report request/response

from abc import ABC, abstractmethod
import click
import json
import logging
import requests

from scanapi.settings import SETTINGS

logger = logging.getLogger(__name__)


class Reporter(ABC):
    def __init__(self, file_path=None):
        self.file_path = file_path

    def write(self, responses):
        if self.file_path:
            logger.info("Writing documentation")
            # Clear the document
            open(self.file_path, "w").close()
            self.docs = open(self.file_path, "w", newline="\n")

        for response in responses:
            self.report_request(response.request)
            self.report_response(response)

        if self.file_path:
            self.docs.close()
            logger.info("The documentation was generated successfully.")
            logger.info(f"It is available at {SETTINGS['docs_path']}")

    @abstractmethod
    def report_request(self, request):
        pass

    @abstractmethod
    def report_response(self, response):
        pass


class ConsoleReporter(Reporter):
    def report_request(self, request):
        logger.info(request.url)

    def report_response(self, response):
        logger.info(f"{response.status_code}\n")


class MarkdownReporter(Reporter):
    def write(self, responses):
        from jinja2 import Environment, PackageLoader, select_autoescape

        env = Environment(loader=PackageLoader("scanapi", "templates"))
        template = env.get_template("markdown.jinja")
        content = template.render(responses=responses)

        with open("docs-jinja.md", "w", newline="\n") as doc_jinja:
            doc_jinja.write(content)

    def report_request(self, request):
        self.docs.write(f"\n## Request: {request.method} {request.url}\n")
        self.write_headers(request.headers)

        if not request.body:
            return

        serialized_body = json.loads(request.body)
        if not serialized_body:
            return

        self.docs.write("\nBODY:\n")
        self.build_code_block(json.dumps(serialized_body, indent=2))

    def report_response(self, response):
        self.docs.write(f"\n### Response: {response.status_code}\n")
        self.docs.write(f"\nIs redirect? {response.is_redirect}\n")
        self.write_headers(response.headers)

        if not response.content:
            return

        self.docs.write("\nContent:\n")

        try:
            code = json.dumps(response.json(), indent=2)
            self.build_code_block(code)
        except ValueError:
            self.build_code_block(str(response.content))

    def build_code_block(self, code):
        self.docs.write(
            """<details><summary></summary><p>
            \n```\n"""
        )
        self.docs.write(code)
        self.docs.write("""\n```\n</p></details>\n""")

    def write_headers(self, headers):
        headers = self.hide_headers_sensitive_info(headers)

        self.docs.write("\nHEADERS:\n")
        if not headers:
            self.docs.write("None\n")
            return

        self.build_code_block(json.dumps(dict(headers), indent=2))

    def hide_headers_sensitive_info(self, headers):
        if "docs" in SETTINGS and "hide" in SETTINGS["docs"]:
            to_hide = SETTINGS["docs"]["hide"]
        else:
            to_hide = {}

        if to_hide and "headers" in to_hide:
            keys_to_hide = to_hide["headers"]
            for key in keys_to_hide:
                headers[key] = "<sensitive information>"

            return headers

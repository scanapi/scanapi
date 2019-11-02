#!/usr/bin/env python3

# TODO LIST
# extrair private methods comuns entre request e response
# matar param doc
# retornar ao inves de imprimir: separar responsabilidade entre "reportar" e "escrever"
# pensar se vale a pena trazer o hide_sensitive_informations pra dentro do report request/response

from abc import ABC, abstractmethod
import click
import json
import logging
import requests

from scanapi.settings import SETTINGS

logger = logging.getLogger(__name__)


class Reporter(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def write(self, responses):
        pass

    @abstractmethod
    def report_request(self, request, docs):
        pass

    @abstractmethod
    def report_response(self, response, docs):
        pass

    @abstractmethod
    def build_code_block(self, code):
        pass


class MarkdownReporter(Reporter):
    def write(self, responses):
        logger.info("Writing documentation")
        open(self.file_path, "w").close()

        for response in responses:
            request = response.request

            with open(self.file_path, "a", newline="\n") as docs:
                self.report_request(request, docs)
                self.report_response(response, docs)

        logger.info("The documentation was generated successfully.")
        logger.info(f"It is available at {SETTINGS['docs_path']}")

    def report_request(self, request, docs):
        docs.write(f"\n## Request: {request.method} {request.url}\n")

        # self.write_headers()
        headers = request.headers
        headers = self.hide_headers_sensitive_info(headers)

        docs.write("\nHEADERS:\n")
        if not headers:
            docs.write("None\n")
            return

        self.build_code_block(json.dumps(dict(headers), indent=2), docs)

        # self.write_body()
        if not request.body:
            return

        serialized_body = json.loads(request.body)
        if not serialized_body:
            return

        docs.write("\nBODY:\n")
        self.build_code_block(json.dumps(serialized_body, indent=2), docs)

    def report_response(self, response, docs):
        docs.write(f"\n### Response: {response.status_code}\n")

        # self.write_is_redirect()
        docs.write(f"\nIs redirect? {response.is_redirect}\n")

        # self.write_headers()
        headers = response.headers
        headers = self.hide_headers_sensitive_info(headers)

        docs.write("\nHEADERS:\n")
        if not headers:
            docs.write("None\n")
            return

        self.build_code_block(json.dumps(dict(headers), indent=2), docs)

        # self.write_content()
        if not response.content:
            return

        docs.write("\nContent:\n")

        try:
            code = json.dumps(response.json(), indent=2)
            self.build_code_block(code, docs)
        except ValueError:
            self.build_code_block(str(response.content), docs)

    def build_code_block(self, code, docs):
        docs.write(
            """<details><summary></summary><p>
            \n```\n"""
        )
        docs.write(code)
        docs.write("""\n```\n</p></details>\n""")

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

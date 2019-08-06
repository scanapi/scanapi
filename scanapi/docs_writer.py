#!/usr/bin/env python3

import click
import json
import logging
import requests

from scanapi.settings import SETTINGS

logger = logging.getLogger(__name__)


class CodeBlock:
    def __init__(self, file):
        self.file = file

    def __enter__(self):
        self.file.write(
            """<details><summary></summary><p>
            \n```\n"""
        )

    def __exit__(self, type, value, traceback):
        self.file.write("""\n```\n</p></details>\n""")


class HTTPMessageWriter:
    def __init__(self, message, file):
        self.message = message
        self.file = file

    def write_headers(self):
        headers = self.message.headers
        headers = self.hide_headers_sensitive_info(headers)

        self.file.write("\nHEADERS:\n")
        if not headers:
            self.file.write("None\n")
            return

        with CodeBlock(self.file):
            json.dump(dict(headers), self.file, indent=2)

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


class RequestWriter(HTTPMessageWriter):
    def __init__(self, request, file):
        HTTPMessageWriter.__init__(self, request, file)
        self.request = request

    def write(self):
        self.file.write(
            "\n## Request: {} {}\n".format(self.request.method, self.request.url)
        )
        self.write_headers()
        self.write_body()

    def write_body(self):
        if not self.request.body:
            return

        serialized_body = json.loads(self.request.body)
        if not serialized_body:
            return

        self.file.write("\nBODY:\n")
        with CodeBlock(self.file):
            json.dump(serialized_body, self.file, indent=2)


class ResponseWriter(HTTPMessageWriter):
    def __init__(self, response, file):
        HTTPMessageWriter.__init__(self, response, file)
        self.response = response

    def write(self):
        self.file.write("\n### Response: {}\n".format(self.response.status_code))
        self.write_is_redirect()
        self.write_headers()
        self.write_content()

    def write_is_redirect(self):
        self.file.write("\nIs redirect? {}\n".format(self.response.is_redirect))

    def write_content(self):
        if not self.response.content:
            return

        self.file.write("\nContent:\n")

        with CodeBlock(self.file):
            try:
                json.dump(self.response.json(), self.file, indent=2)
            except ValueError:
                self.file.write(str(self.response.content))


class DocsWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def write(self, responses):
        logger.info("Writing documentation")
        open(self.file_path, "w").close()

        [self.write_response(response) for response in responses]

        logger.info("The documentation was generated successfully.")
        logger.info("It is available at {}".format(SETTINGS["docs_path"]))

    def write_response(self, response):
        request = response.request

        with open(self.file_path, "a", newline="\n") as docs:
            RequestWriter(request, docs).write()
            ResponseWriter(response, docs).write()

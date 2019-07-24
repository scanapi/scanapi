#!/usr/bin/env python3

import json
import logging
import requests


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
        self.file.write("\nHEADERS:\n")
        if not self.message.headers:
            self.file.write("None\n")
            return

        with CodeBlock(self.file):
            json.dump(dict(self.message.headers), self.file, indent=2)


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
        self.file.write("\nBODY:\n")

        if not self.request.body:
            self.file.write("None\n")
            return

        with CodeBlock(self.file):
            json.dump(dict(self.request.body), self.file, indent=2)


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
        self.file.write("\nContent:\n")

        if not self.response.content:
            self.file.write("None\n")
            return

        with CodeBlock(self.file):
            try:
                json.dump(self.response.json(), self.file, indent=2)
            except ValueError:
                self.file.write(str(self.response.content))


class DocsWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def write(self, responses):
        open(self.file_path, "w").close()
        [self.write_response(response) for response in responses]

    def write_response(self, response):
        request = response.request

        with open(self.file_path, "a", newline="\n") as docs:
            RequestWriter(request, docs).write()
            ResponseWriter(response, docs).write()

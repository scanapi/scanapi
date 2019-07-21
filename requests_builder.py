#!/usr/bin/env python3
import requests
import yaml

from variable_parser import populate_dict, populate_str


class RequestsBuilder:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as stream:
            try:
                self.api = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def all_responses(self):
        responses = []
        url = populate_str(self.api["base-url"])
        headers = self.merge_headers({}, self.api)

        for endpoint in self.api["endpoints"]:
            headers = self.merge_headers(headers, endpoint)
            url = self.merge_url_path(url, endpoint)

            for request in endpoint["requests"]:
                headers = self.merge_headers(headers, request)
                url = self.merge_url_path(url, request)

                if request["method"].lower() == "get":
                    responses.append(self.get_request(url, headers))

        return responses

    def merge_url_path(self, path, node):
        if "path" not in node:
            return path

        populated_node_path = populate_str(node["path"])
        return "/".join(s.strip("/") for s in [path, populated_node_path])

    def merge_headers(self, headers, node):
        if "headers" not in node:
            return headers

        return {**headers, **populate_dict(node["headers"])}

    def get_request(self, url, headers):
        return requests.get(url, headers=headers)

#!/usr/bin/env python3
import requests
import yaml


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
        url = self.api["base-url"]
        headers = self.api["headers"]

        for endpoint in self.api["endpoints"]:
            headers = self.merge_headers(headers, endpoint)
            url = self.merge_url_path(url, endpoint)

            for request in endpoint["requests"]:
                headers = self.merge_headers(headers, request)
                url = self.merge_url_path(url, request)

                if request["method"].lower() == "get":
                    responses.append(self.get_request(url, headers))

        return responses

    def join_url_paths(self, paths):
        return "/".join(s.strip("/") for s in paths)

    def merge_url_path(self, path, node):
        if "path" not in node:
            return path

        return "/".join(s.strip("/") for s in [path, node["path"]])

    def merge_headers(self, headers, node):
        if "headers" not in node:
            return headers

        return {**headers, **node["headers"]}

    def get_request(self, url, headers):
        return requests.get(url, headers=headers)

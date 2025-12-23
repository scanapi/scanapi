import json
import os

import yaml

from .errors import EmptyOpenAPIFileError, InvalidOpenAPIFileError


def _is_file_empty(file_path: str) -> None:
    if not os.stat(file_path).st_size:
        raise EmptyOpenAPIFileError(file_path)


def _is_valid_openapi_spec(open_api_dict: dict, json_file_path: str) -> None:

    required_general_keys = ["info", "host", "schemes", "basePath", "paths"]

    all_general_keys = all(
        key in open_api_dict for key in required_general_keys
    )

    if not all_general_keys or "title" not in open_api_dict["info"]:
        raise InvalidOpenAPIFileError(json_file_path)


def openapi_to_yaml(json_file_path: str) -> None:
    """
    Converts a OpenAPI JSON file into a ScanAPI friendly YAML file.
    :param json_file_path: Path to the OpenAPI File
    :return: None
    """
    _is_file_empty(json_file_path)

    with open(json_file_path, "r") as file:
        openapi_specs = json.load(file)

    _is_valid_openapi_spec(openapi_specs, json_file_path)

    base_yaml: dict = {
        "api": {"endpoints": [{"name": None, "path": None, "requests": []}]}
    }

    endpoints = base_yaml["api"]["endpoints"][0]
    requests = endpoints["requests"]

    endpoints["name"] = openapi_specs["info"]["title"]
    endpoints["path"] = (
        openapi_specs["schemes"][0]
        + "://"
        + openapi_specs["host"]
        + openapi_specs["basePath"]
    )

    for route_name, data in openapi_specs["paths"].items():
        for method_name, endpoint_info in data.items():
            api_target = {
                "name": endpoint_info["summary"],
                "path": route_name,
                "method": method_name,
            }
            requests.append(api_target)

    with open("./api.yaml", "w") as file:
        file.write(
            yaml.dump(
                base_yaml, default_flow_style=False, sort_keys=False, indent=4
            )
        )

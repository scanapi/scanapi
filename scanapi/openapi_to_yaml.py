import json
import os

import yaml
from openapi_spec_validator import validate_spec, validate_v2_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError

from scanapi.errors import (
    EmptyJsonFileError,
    InvalidJsonFileError,
    InvalidOpenAPISpecError,
    NotAJsonFileError,
)


def _is_json_file(file_path: str) -> bool:
    if file_path.lower().endswith(".json"):
        return True
    raise NotAJsonFileError(file_path)


def _is_json_file_empty(file_path: str) -> bool:
    if os.stat(file_path).st_size:
        return False
    raise EmptyJsonFileError(file_path)


def _validate_json_file(file_path):
    if _is_json_file(file_path) and not _is_json_file_empty(file_path):
        try:
            with open(file_path, "r") as file:
                openapi_specs = json.load(file)
            return openapi_specs
        except ValueError:
            pass

        raise InvalidJsonFileError


def _validate_openapi_spec(open_api_dict: dict):
    try:
        validate_spec(open_api_dict)
        return True
    except OpenAPIValidationError:
        pass

    try:
        validate_v2_spec(open_api_dict)
        return True
    except OpenAPIValidationError:
        pass

    raise InvalidOpenAPISpecError


def openapi_to_yaml(json_file_path: str):
    """
    Converts a OpenAPI JSON file into a ScanAPI friendly YAML file.
    :param json_file_path: Path to the OpenAPI File
    :return: None
    """
    openapi_specs = _validate_json_file(json_file_path)

    _validate_openapi_spec(openapi_specs)

    base_yaml = {
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

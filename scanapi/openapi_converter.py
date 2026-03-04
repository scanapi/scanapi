from typing import cast

from prance import ResolvingParser


class OpenAPIConverter:
    """
    Class responsible for parsing an OpenAPI schema and generating
    a skeleton ScanAPI yaml file with correct endpoints, request methods
    and authentication schema.

    Uses [prance](https://github.com/RonnyPfannschmidt/prance) for resolving
    and parsing the OpenAPI schema.

    Attributes:
        spec_path[str]: path to the OpenAPI spec file. Either YAML or JSON.
    """

    SECURITY_SCHEME_TYPES = ("http", "oauth2", "bearer")
    VALID_HTTP_METHODS = (
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "HEAD",
        "OPTIONS",
    )
    BODY_CONTENT_TYPES = (
        "application/x-www-form-urlencoded",
        "application/json",
        "multipart/form-data",
    )

    def __init__(self, spec_path: str):
        self.created_variables: set[str] = set()
        self.specs = self._get_openapi_specs(spec_path)
        self._validate_openapi_spec_version()

    def _get_openapi_specs(self, spec_path: str) -> dict:
        """Leverages [prance](https://github.com/RonnyPfannschmidt/prance) to resolve
        the received OpenAPI spec file.

        Returns:
            [dict]: Parsed OpenAPI specification
        """
        parser = ResolvingParser(spec_path)
        parser.parse()
        return cast(dict, parser.specification)

    def _get_spec_version(self) -> str:
        """Reads the version from parsed specification

        Returns:
            [str]: version string

        Raises:
            [ValueError]: Couldn't find version key on parsed specification"""
        spec_version: str | None = None
        if "openapi" in self.specs:
            spec_version = self.specs.get("openapi")
        elif "swagger" in self.specs:
            spec_version = self.specs.get("swagger")

        if spec_version is None:
            raise ValueError(
                "Could not determine OpenAPI/Swagger specification version!"
            )
        return spec_version

    def _validate_openapi_spec_version(self):
        """Checks whether the received OpenAPI specification is supported by the converter.

        Returns:
            None

        Raises:
            [ValueError]: Unsupported OpenAPI specification version"""
        specs_version = self._get_spec_version()
        print(f"OpenAPI/Swagger version detected: {specs_version}\n")

        if not specs_version.startswith("3"):
            raise ValueError(
                "OpenAPI/Swagger version 3 is required to use this feature."
            )

    def _get_api_name(self) -> str | None:
        """Reads title from the spec info tag.

        Returns:
            [str|None]: Title if present, otherwise None"""
        info = self.specs.get("info", None)
        if info is None:
            return None
        title = info.get("title", None)
        if title is None:
            return None
        return str(title)

    def _get_security_schemes(self) -> list:
        """Gets existing security schema from the OpenAPI specification,
        described using the `securitySchemes` under the top level `components`.

        Reference: <https://swagger.io/docs/specification/v3_0/authentication/#describing-security>

        Returns:
            [list[dict]]: name and type of found security schemes."""
        security_schemes = []
        if (
            "components" in self.specs
            and "securitySchemes" in self.specs["components"]
        ):
            for name, security_scheme in self.specs["components"][
                "securitySchemes"
            ].items():
                if (
                    security_scheme.get("type")
                    not in self.SECURITY_SCHEME_TYPES
                ):
                    continue
                # TODO: we assume oauth2 always uses bearer token
                # which is untrue. see https://swagger.io/docs/specification/v3_0/authentication/
                security_schemes.append(
                    {
                        "name": name,
                        "scheme": security_scheme.get("scheme", "bearer"),
                    }
                )
        return security_schemes

    def _get_required_properties_from_schema(
        self, schema: dict, operation_id: str
    ) -> dict[str, str] | None:
        """
        Formats required properties for a given request body schema as a dictionary.

        Returns:
            [dict|None]: Keys are property names and values are custom variables created using the operation_id and the property name.
        """
        required_properties = None
        if "required" in schema:
            required_properties = {}
            for prop_name in schema["required"]:
                property_variable = operation_id + "_" + prop_name
                required_properties[prop_name] = "${" + property_variable + "}"
                self.created_variables.add(property_variable)
        return required_properties

    def _add_variables_to_path(
        self, path: str, params: list, operation_id: str
    ) -> str:
        parsed_path = path
        for param in params:
            if param["in"] == "query":
                # TODO: this could be later implemented if we have additional
                # information such as expected responses, etc
                continue
            if param["in"] == "path":
                # path param is generally curly braced (/snippets/{id}/) and
                # scanapi expects variable notation (/snippets/${id})
                path_param_name = f"{operation_id}_{param['name']}"
                parsed_path = parsed_path.replace(
                    f"{{{param['name']}}}", "${" + path_param_name + "}"
                )
                self.created_variables.add(path_param_name)
        return parsed_path

    def convert(self, base_url: str) -> dict:
        """
        Runs the convertion algorithm and returns a YAML convertable dictionary.

        :param specs: dictionary representing the OpenAPI specs
        :param base_url: Base URL for the API
        """
        base_yaml: dict = {
            "endpoints": [{"name": None, "path": base_url, "requests": []}]
        }

        api_name = self._get_api_name()
        base_yaml["endpoints"][0]["name"] = api_name

        security_schemes = self._get_security_schemes()

        paths = self.specs.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() not in self.VALID_HTTP_METHODS:
                    continue
                operation_id = get_api_target_name(operation, path, method)
                required_params = get_required_params(operation)
                parsed_path = (
                    path
                    if not required_params
                    else self._add_variables_to_path(
                        path, required_params, operation_id
                    )
                )
                api_target = {
                    "name": operation_id,
                    "path": parsed_path,
                    "method": method,
                }
                api_target["tests"] = get_tests(operation)
                if (
                    "requestBody" in operation
                    and "content" in operation["requestBody"]
                ):
                    api_target_body = None
                    content = operation["requestBody"]["content"]
                    available_content_types = content.keys()
                    # prioritize application/x-www-form-urlencoded over other content types
                    for content_type in self.BODY_CONTENT_TYPES:
                        if content_type in available_content_types:
                            api_target_body = (
                                self._get_required_properties_from_schema(
                                    content[content_type]["schema"],
                                    operation_id,
                                )
                            )
                            break

                    if api_target_body is not None:
                        api_target["body"] = api_target_body
                operation_security = operation.get("security", [])
                if len(operation_security) > 0:
                    for security in operation_security:
                        for name, scopes in security.items():
                            for security_scheme in security_schemes:
                                if security_scheme["name"] == name:
                                    security_type = security_scheme["scheme"]
                                    if security_type == "bearer":
                                        api_target["headers"] = {
                                            "Authorization": "Bearer ${bearer_token}"
                                        }
                                        self.created_variables.add(
                                            "bearer_token"
                                        )
                                    elif security_type == "basic":
                                        api_target["headers"] = {
                                            "Authorization": "Basic ${basic_auth_token}"
                                        }
                                        self.created_variables.add(
                                            "basic_auth_token"
                                        )
                                    break
                base_yaml["endpoints"][0]["requests"].append(api_target)

        if len(self.created_variables) > 0:
            print(
                "The following variables were created in the generated ScanAPI YAML file:"
            )
            for variable in self.created_variables:
                print("- ${" + variable + "}")
            print(
                "See https://scanapi.dev/docs_v1/specification/custom_variables and https://scanapi.dev/docs_v1/specification/environment_variables for more information.\n"
            )
        return base_yaml


def get_api_target_name(operation: dict, path: str, method: str) -> str:
    """
    Generates a variable friendly name for a request. Prioritizes the summary,
    then operationId and, if none is defined, fall back to using the method_path format.

    Changes all slashes and spaces to underscores.

    Returns:
        [str]: generated target name
    """
    return (
        str(
            operation.get(
                "summary", operation.get("operationId", f"{method}_{path}")
            )
        )
        .replace("/", "_")
        .replace(" ", "_")
    )


# focuses on the minimal required parameters for performing the request
def get_required_params(operation: dict) -> list:
    params = []
    if "parameters" in operation:
        for param in operation["parameters"]:
            if param.get("required", False):
                params.append(
                    {
                        "name": param["name"],
                        "in": param.get(
                            "in"
                        ),  # TODO: check if there is a default value for `in`
                    }
                )
    return params


# focuses on successful responses for minimal smoke testing
def get_tests(operation: dict) -> list:
    tests = []
    if "responses" in operation:
        for status_code, details in operation["responses"].items():
            # Handle string response keys from OpenAPI such as 2XX
            # see https://swagger.io/docs/specification/v3_0/describing-responses/#http-status-codes
            if not status_code.isdigit():
                continue
            if not status_code.startswith("2"):
                continue
            # details is a dict with content (dict) and description (str)
            tests.append(
                {
                    "name": f"status_code_is_{status_code}",
                    "assert": f"${{{{response.status_code == {status_code}}}}}",
                }
            )
    return tests

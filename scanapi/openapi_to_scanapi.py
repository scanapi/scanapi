from typing import cast

from prance import ResolvingParser

created_variables: set[str] = set()

def get_spec_version(specs: dict) -> str:
    spec_version: str | None = None
    if "openapi" in specs:
        spec_version = specs.get("openapi")
    elif "swagger" in specs:
        spec_version = specs.get("swagger")
    
    if spec_version is None:
        raise ValueError("Could not determine OpenAPI/Swagger specification version!")
    return spec_version

def get_api_name(specs: dict) -> str:
    return str(specs["info"]["title"])

def get_api_target_name(operation: dict, path: str) -> str:
    return str(operation.get(
        "summary", operation.get(
            "operationId", path
        )
    )).replace("/", "_").replace(" ", "_")

def get_openapi_specs(openapi_path: str) -> dict:
    parser = ResolvingParser(openapi_path)
    parser.parse()
    return cast(dict, parser.specification)

def openapi_to_scanapi(specs: dict, base_url: str) -> dict:
    """
    Converts a OpenAPI specification into a ScanAPI friendly YAML file.
    :param specs: dictionary representing the OpenAPI specs
    :param base_url: Base URL for the API
    :return: ScanAPI YAML file
    """
    base_yaml: dict = {
        "endpoints": [{"name": None, "path": base_url, "requests": []}]
    }

    specs_version = get_spec_version(specs)
    print(f"OpenAPI/Swagger version detected: {specs_version}\n")

    if not specs_version.startswith("3"):
        raise ValueError("OpenAPI/Swagger version 3 is required to use this feature.")
    api_name = get_api_name(specs)
    base_yaml["endpoints"][0]["name"] = api_name

    security_schemes = get_security_schemes(specs)

    paths = specs["paths"]
    for path, path_item in paths.items():
        for method, operation in path_item.items():
            operation_id = get_api_target_name(operation, path)
            required_params = get_required_params(operation)
            parsed_path = path if not required_params else add_variables_to_path(path, required_params, operation_id)
            api_target = {
                "name": operation_id,
                "path": parsed_path,
                "method": method
            }
            api_target["tests"] = get_tests(operation)
            if "requestBody" in operation and "content" in operation["requestBody"]:
                api_target_body = None

                
                # prioritize application/x-www-form-urlencoded over other content types
                available_content_types = operation["requestBody"]["content"].keys()
                if "application/x-www-form-urlencoded" in available_content_types:
                    api_target_body = get_required_properties_from_schema(operation["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"], operation_id)
                elif "application/json" in available_content_types:
                    api_target_body = get_required_properties_from_schema(operation["requestBody"]["content"]["application/json"]["schema"], operation_id)
                elif "multipart/form-data" in available_content_types:
                    api_target_body = get_required_properties_from_schema(operation["requestBody"]["content"]["multipart/form-data"]["schema"], operation_id)

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
                                    created_variables.add("bearer_token")
                                elif security_type == "basic":
                                    api_target["headers"] = {
                                        "Authorization": "Basic ${basic_auth_token}"
                                    }
                                    created_variables.add("basic_auth_token")
                                break
            base_yaml["endpoints"][0]["requests"].append(api_target)
    
    if len(created_variables) > 0:
        print("The following variables were created in the generated ScanAPI YAML file:")
        for variable in created_variables:
            print("- ${" + variable + "}")
        print("See https://scanapi.dev/docs_v1/specification/custom_variables and https://scanapi.dev/docs_v1/specification/environment_variables for more information.\n")
    return base_yaml

# returns the required properties from a schema
def get_required_properties_from_schema(schema: dict, operation_id: str) -> dict[str, str]:
    required_properties = None
    if "required" in schema:
        required_properties = {}
        for property in schema["required"]:
            property_variable = operation_id + "_" + property
            required_properties[property] = "${" + property_variable + "}"
            created_variables.add(property_variable)
    return required_properties

def add_variables_to_path(path: str, params: list, operation_id: str) -> str:
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
            parsed_path = parsed_path.replace(f"{{{param['name']}}}", "${" + path_param_name + "}")
            created_variables.add(path_param_name)
    return parsed_path

# focuses on the minimal required parameters for performing the request
def get_required_params(operation: dict) -> list:
    params = []
    if "parameters" in operation:
        for param in operation["parameters"]:
            if param.get("required", False):
                params.append({
                    "name": param["name"],
                    "in": param.get("in"), # TODO: check if there is a default value for `in`
                })
    return params

# focuses on successful responses for minimal smoke testing
def get_tests(operation: dict) -> list:
    tests = []
    if "responses" in operation:
        for status_code, details in operation["responses"].items():
            if not status_code.startswith("2"):
                continue
            # details is a dict with content (dict) and description (str)
            tests.append({
                "name": f"status_code_is_{status_code}",
                "assert": f"${{{{response.status_code == {status_code}}}}}"
            })
    return tests

def get_security_schemes(specs: dict) -> list:
    security_schemes = []
    if "components" in specs and "securitySchemes" in specs["components"]:
        for name, security_scheme in specs["components"]["securitySchemes"].items():
            if security_scheme["type"] not in ["http", "oauth2"]:
                continue
            # TODO: we assume oauth2 always uses bearer token
            # which is untrue. see https://swagger.io/docs/specification/v3_0/authentication/
            security_schemes.append({
                "name": name,
                "scheme": security_scheme.get("scheme", "bearer")
            })
    return security_schemes
import json
import yaml


def openapi_to_yaml(json_file_path: str):
    """
    Converts a OpenAPI JSON file into a ScanAPI friendly YAML file.
    :param json_file_path: Path to the OpenAPI File
    :return: None
    """
    with open(json_file_path, 'r') as file:
        openapi_specs = json.load(file)

    base_yaml = {"api":
                     {"endpoints":
                          [{"name": None,
                            "path": None,
                            "requests": []
                            }]
                      }
                 }

    endpoints = base_yaml['api']['endpoints'][0]
    requests = endpoints['requests']

    endpoints['name'] = openapi_specs['info']['title']
    endpoints['path'] = openapi_specs["schemes"][0] + '://' + openapi_specs["host"] + openapi_specs["basePath"]

    for route_name, data in openapi_specs['paths'].items():
        for method_name, endpoint_info in data.items():
            api_target = {"name": endpoint_info['summary'], "path": route_name, "method": method_name}
            requests.append(api_target)

    with open('./api.yaml', 'w') as file:
        file.write(yaml.dump(base_yaml, default_flow_style=False, sort_keys=False, indent=4))

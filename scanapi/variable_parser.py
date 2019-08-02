import re
import yaml
from scanapi.settings import SETTINGS


variable_pattern = re.compile("(^\\${)(\\w*)(}$)")  # ${<variable_name>}
python_code_pattern = re.compile("(^\\${{)(.*)(}}$)")  # ${{<python_code>}}
responses = {}


def populate_dict(element, node):
    populated_dict = {}
    for key, value in element.items():
        populated_dict[key] = populate_str(value, node)

    return populated_dict


def populate_str(sequence, node):
    sequence = str(sequence)

    if is_variable(sequence):
        return get_variable_value(sequence, node)

    if is_python_code(sequence):
        return get_python_code_value(sequence)

    return sequence


def is_variable(sequence):
    return variable_pattern.search(sequence) is not None


def is_python_code(sequence):
    return python_code_pattern.search(sequence) is not None


def get_variable_value(sequence, node):
    variable_name = get_variable_name(sequence)

    if variable_name.isupper():
        return SETTINGS["env_vars"][variable_name]

    if type(node).__name__ == "RequestNode":
        return node.parent.custom_vars[variable_name]


def get_variable_name(sequence):
    match = variable_pattern.search(sequence)
    if not match:
        return
    return match.group(2)


def get_python_code_value(sequence):
    match = python_code_pattern.search(sequence)
    if not match:
        return

    return str(eval(match.group(2)))


def save_response(response_id, response):
    responses[response_id] = response

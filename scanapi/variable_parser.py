import re
import yaml
from scanapi.settings import SETTINGS


variable_pattern = re.compile("(^\\${)(\\w*)(}$)")  # ${<variable_name>}
python_code_pattern = re.compile("(^\\${{)(.*)(}}$)")  # ${{<python_code>}}
custom_variables = {}
responses = {}


def populate_dict(element):
    populated_dict = {}
    for key, value in element.items():
        populated_dict[key] = populate_str(value)

    return populated_dict


def populate_str(sequence):
    sequence = str(sequence)

    if is_variable(sequence):
        return get_variable_value(sequence)

    if is_python_code(sequence):
        return get_python_code_value(sequence)

    return sequence


def is_variable(sequence):
    return variable_pattern.search(sequence) is not None


def is_python_code(sequence):
    return python_code_pattern.search(sequence) is not None


def get_variable_value(sequence):
    variable_name = get_variable_name(sequence)

    if variable_name.isupper():
        return SETTINGS["env_vars"][variable_name]

    return custom_variables[variable_name]


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


def save_variable(name, value):
    custom_variables[name] = populate_str(value)


def save_response(response_id, response):
    responses[response_id] = response

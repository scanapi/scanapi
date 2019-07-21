import re
import yaml
from settings import SETTINGS


variable_pattern = re.compile("(^\\${)(\\w*)(}$)")  # ${<variable_name>}
python_code_pattern = re.compile("(^\\${{)(.*)(}}$)")  # ${{<python_code>}}
custom_variables = {}


def populate_dict(element):
    populated_dict = {}
    for key, value in element.items():
        populated_dict[key] = populate_str(value)

    return populated_dict


def populate_str(sequence):
    variable_name = get_variable_name(sequence)

    if not variable_name:
        return sequence

    if variable_name.isupper():
        return SETTINGS["env_vars"][variable_name]

    return custom_variables[variable_name]


def get_variable_name(sequence):
    match = variable_pattern.search(sequence)
    if not match:
        return
    return match.group(2)


def save_variable(name, value):
    custom_variables[name] = populate_str(value)

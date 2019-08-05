from enum import Enum
import re
import yaml
from scanapi.settings import SETTINGS


variable_pattern = re.compile("(^\\${)(\\w*)(}$)")  # ${<variable_name>}
python_code_pattern = re.compile("(^\\${{)(.*)(}}$)")  # ${{<python_code>}}
responses = {}


class EvaluationType(Enum):
    ENV_VAR = 1
    CUSTOM_VAR = 2
    PYTHON_CODE = 3


def evaluate(type, element, node=None):
    if isinstance(element, dict):
        return evaluate_dict(type, element, node)

    element = str(element)

    if type == EvaluationType.ENV_VAR:
        return evaluate_env_var(element)

    if type == EvaluationType.CUSTOM_VAR:
        return evaluate_custom_var(element, node)

    if type == EvaluationType.PYTHON_CODE:
        return evaluate_python_code(element)

    return element


def evaluate_dict(type, element, node):
    evaluated_dict = {}
    for key, value in element.items():
        evaluated_dict[key] = evaluate(type, value, node)

    return evaluated_dict


def evaluate_env_var(sequence):
    if not is_env_var(sequence):
        return sequence

    variable_name = get_variable_name(sequence)
    return SETTINGS["env_vars"][variable_name]


def evaluate_custom_var(sequence, node):
    if not is_custom_var(sequence) or not node:
        return sequence

    variable_name = get_variable_name(sequence)
    return node.parent.custom_vars[variable_name]


def evaluate_python_code(sequence):
    if not is_python_code(sequence):
        return sequence

    return get_python_code_value(sequence)


def is_variable(sequence):
    return variable_pattern.search(sequence) is not None


def is_custom_var(sequence):
    return is_variable(sequence) and sequence.islower()


def is_env_var(sequence):
    return is_variable(sequence) and sequence.isupper()


def is_python_code(sequence):
    return python_code_pattern.search(sequence) is not None


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


def save_response(request_id, response):
    responses[request_id] = response

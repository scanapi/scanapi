from enum import Enum
import logging
import os
import re
import sys
import yaml

from scanapi.errors import BadConfigurationError

logger = logging.getLogger(__name__)
variable_pattern = re.compile("(\\w*)(\\${)(\\w*)(})(\\w*)")  # ${<variable_name>}
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
        try:
            return evaluate_env_var(element)
        except BadConfigurationError as e:
            logger.error(e)
            sys.exit()

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
    match = variable_pattern.search(sequence)

    if not match or match.group(3).islower():
        return sequence

    variable_name = match.group(3)
    try:
        variable_value = os.environ[variable_name]
    except KeyError as e:
        raise BadConfigurationError(e)

    return evaluate_var(sequence, variable_name, variable_value)


def evaluate_custom_var(sequence, node):
    match = variable_pattern.search(sequence)

    if not match or match.group(3).isupper() or not node:
        return sequence

    variable_name = match.group(3)
    variable_value = evaluate(
        EvaluationType.PYTHON_CODE, node.parent.custom_vars[variable_name]
    )

    return evaluate_var(sequence, variable_name, variable_value)


def evaluate_var(sequence, variable_name, variable_value):
    sequence = re.sub(variable_name, variable_value, sequence)
    sequence = re.sub(r"\${", "", sequence)
    sequence = re.sub(r"}", "", sequence)

    return sequence


def evaluate_python_code(sequence):
    match = python_code_pattern.search(sequence)

    if not match:
        return sequence

    code = match.group(2)
    return str(eval(code))


def save_response(request_id, response):
    responses[request_id] = response

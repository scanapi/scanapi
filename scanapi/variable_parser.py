from enum import Enum
import logging
import os
import re
import sys
import yaml

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError

# Available imports to be used dinamically in the api spec
import datetime
import math
import random
import time
import uuid

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

    if isinstance(element, list):
        return evaluate_list(type, element, node)

    if not isinstance(element, str):
        return element

    if type == EvaluationType.ENV_VAR:
        try:
            return evaluate_env_var(element)
        except BadConfigurationError as e:
            logger.error(e)
            sys.exit()

    if type == EvaluationType.CUSTOM_VAR:
        return evaluate_custom_var(element, node)

    if type == EvaluationType.PYTHON_CODE:
        try:
            return evaluate_python_code(element)
        except InvalidPythonCodeError as e:
            logger.error(e)
            sys.exit()

    return element


def evaluate_dict(type, element, node):
    evaluated_dict = {}
    for key, value in element.items():
        evaluated_dict[key] = evaluate(type, value, node)

    return evaluated_dict


def evaluate_list(type, elements, node):
    evaluated_list = []
    for item in elements:
        evaluated_list.append(evaluate(type, item, node))

    return evaluated_list


def evaluate_env_var(sequence):
    matches = variable_pattern.finditer(sequence)

    if not matches:
        return sequence

    for match in matches:
        variable_name = match.group(3)

        if variable_name.islower():
            continue

        try:
            variable_value = os.environ[variable_name]
        except KeyError as e:
            raise BadConfigurationError(e)

        sequence = evaluate_var(sequence, match.group(), variable_value)

    return sequence


def evaluate_custom_var(sequence, node):
    matches = variable_pattern.finditer(sequence)

    if not matches or not node:
        return sequence

    for match in matches:
        variable_name = match.group(3)

        if variable_name.isupper():
            continue

        variable_value = evaluate(
            EvaluationType.PYTHON_CODE, node.parent.custom_vars[match.group(3)]
        )

        sequence = evaluate_var(sequence, match.group(), variable_value)

    return sequence


def evaluate_var(sequence, variable, variable_value):
    variable = re.escape(variable)
    return re.sub(variable, variable_value, sequence)


def evaluate_python_code(sequence):
    match = python_code_pattern.search(sequence)

    if not match:
        return sequence

    code = match.group(2)

    try:
        return str(eval(code))
    except Exception as e:
        raise InvalidPythonCodeError(str(e))


def save_response(request_id, response):
    responses[request_id] = response

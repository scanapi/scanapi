from enum import Enum
import logging
import os
import re
import sys
import yaml

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError


logger = logging.getLogger(__name__)
variable_pattern = re.compile(
    r"(?P<something_before>\w*)(?P<start>\${)(?P<variable>\w*)(?P<end>})(?P<something_after>\w*)"
)  # ${<variable>}
python_code_pattern = re.compile(
    r"(?P<something_before>\w*)(?P<start>\${{)(?P<python_code>.*)(?P<end>}})(?P<something_after>\w*)"
)  # ${{<python_code>}}


def evaluate(api_tree, element):
    if isinstance(element, dict):
        return evaluate_dict(api_tree, element)

    if isinstance(element, list):
        return evaluate_list(api_tree, element)

    if not isinstance(element, str):
        return element

    return evaluate_str(api_tree, element)


def evaluate_dict(type, element):
    evaluated_dict = {}
    for key, value in element.items():
        evaluated_dict[key] = evaluate(type, value)

    return evaluated_dict


def evaluate_list(type, elements):
    evaluated_list = []
    for item in elements:
        evaluated_list.append(evaluate(type, item))

    return evaluated_list


def evaluate_str(api_tree, sequence):
    try:
        sequence = evaluate_env_var(sequence)
    except BadConfigurationError as e:
        logger.error(e)
        sys.exit()

    sequence = evaluate_custom_var(api_tree, sequence)

    if not api_tree.responses:
        return sequence

    try:
        return evaluate_python_code(api_tree, sequence)
    except InvalidPythonCodeError as e:
        logger.error(e)
        sys.exit()


def evaluate_env_var(sequence):
    matches = variable_pattern.finditer(sequence)

    if not matches:
        return sequence

    for match in matches:
        variable_name = match.group("variable")

        if variable_name.islower():
            continue

        try:
            variable_value = os.environ[variable_name]
        except KeyError as e:
            raise BadConfigurationError(e)

        sequence = evaluate_var(sequence, match.group(), variable_value)

    return sequence


def evaluate_custom_var(api_tree, sequence):
    matches = variable_pattern.finditer(sequence)

    if not matches:
        return sequence

    for match in matches:
        variable_name = match.group("variable")

        if variable_name.isupper():
            continue

        if not api_tree.custom_vars.get(variable_name):
            continue

        variable_value = evaluate(api_tree, api_tree.custom_vars[variable_name])
        sequence = evaluate_var(sequence, match.group(), variable_value)

    return sequence


def evaluate_var(sequence, variable, variable_value):
    variable = re.escape(variable)
    return re.sub(variable, variable_value, sequence)


def evaluate_python_code(api_tree, sequence):
    # Available imports to be used dinamically in the api spec
    import datetime
    import math
    import random
    import time
    import uuid

    match = python_code_pattern.search(sequence)

    if not match:
        return sequence

    code = match.group("python_code")
    responses = api_tree.responses

    try:
        python_code_value = str(eval(code))
        return evaluate_var(sequence, match.group(), python_code_value)
    except Exception as e:
        raise InvalidPythonCodeError(str(e))

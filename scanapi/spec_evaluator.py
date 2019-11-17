import logging
import os
import re
import sys
from types import SimpleNamespace

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError


logger = logging.getLogger(__name__)
variable_pattern = re.compile(
    r"(?P<something_before>\w*)(?P<start>\${)(?P<variable>\w*)(?P<end>})(?P<something_after>\w*)"
)  # ${<variable>}
python_code_pattern = re.compile(
    r"(?P<something_before>\w*)(?P<start>\${{)(?P<python_code>.*)(?P<end>}})(?P<something_after>\w*)"
)  # ${{<python_code>}}


class SpecEvaluator:
    def __init__(self, api_tree):
        self.api_tree = api_tree

    def evaluate(self, element):
        if isinstance(element, dict):
            return self.evaluate_dict(element)

        if isinstance(element, list):
            return self.evaluate_list(element)

        if not isinstance(element, str):
            return element

        return self.evaluate_string(element)

    def evaluate_dict(self, element):
        evaluated_dict = {}
        for key, value in element.items():
            evaluated_dict[key] = self.evaluate(value)

        return evaluated_dict

    def evaluate_list(self, elements):
        evaluated_list = []
        for item in elements:
            evaluated_list.append(self.evaluate(item))

        return evaluated_list

    def evaluate_string(self, sequence):
        try:
            sequence = self.evaluate_env_var(sequence)
        except BadConfigurationError as e:
            logger.error(e)
            sys.exit()

        sequence = self.evaluate_custom_var(sequence)

        if not self.api_tree.responses:
            return sequence

        try:
            return self.evaluate_python_code(sequence)
        except InvalidPythonCodeError as e:
            logger.error(e)
            sys.exit()

    def evaluate_env_var(self, sequence):
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

            sequence = self.replace_var_with_value(
                sequence, match.group(), variable_value
            )

        return sequence

    def evaluate_custom_var(self, sequence):
        matches = variable_pattern.finditer(sequence)

        if not matches:
            return sequence

        for match in matches:
            variable_name = match.group("variable")

            if variable_name.isupper():
                continue

            if not self.api_tree.custom_vars.get(variable_name):
                continue

            variable_value = self.evaluate(self.api_tree.custom_vars[variable_name])
            sequence = self.replace_var_with_value(
                sequence, match.group(), variable_value
            )

        return sequence

    def evaluate_python_code(self, sequence):
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
        responses = SimpleNamespace(**self.api_tree.responses)

        try:
            python_code_value = str(eval(code))
            return self.replace_var_with_value(
                sequence, match.group(), python_code_value
            )
        except Exception as e:
            raise InvalidPythonCodeError(str(e))

    def replace_var_with_value(self, sequence, variable, variable_value):
        variable = re.escape(variable)
        return re.sub(variable, variable_value, sequence)

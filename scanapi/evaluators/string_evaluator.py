import logging
import os
import re
import sys

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.evaluators.code_evaluator import CodeEvaluator

logger = logging.getLogger(__name__)
variable_pattern = re.compile(
    r"(?P<something_before>\w*)(?P<start>\${)(?P<variable>\w*)(?P<end>})(?P<something_after>\w*)"
)  # ${<variable>}


class StringEvaluator:
    def __init__(self, spec_evaluator):
        self.spec_evaluator = spec_evaluator
        self.api_tree = spec_evaluator.api_tree
        self.code_evaluator = CodeEvaluator(self)

    def evaluate(self, sequence):
        try:
            sequence = self.evaluate_env_var(sequence)
        except BadConfigurationError as e:
            logger.error(e)
            sys.exit()

        sequence = self.evaluate_custom_var(sequence)

        if not self.api_tree.responses:
            return sequence

        try:
            return self.code_evaluator.evaluate(sequence)
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

            variable_value = self.spec_evaluator.evaluate(
                self.api_tree.custom_vars[variable_name]
            )
            sequence = self.replace_var_with_value(
                sequence, match.group(), variable_value
            )

        return sequence

    def replace_var_with_value(self, sequence, variable, variable_value):
        variable = re.escape(variable)
        return re.sub(variable, variable_value, sequence)

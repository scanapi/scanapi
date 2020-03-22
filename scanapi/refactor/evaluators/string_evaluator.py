import os
import re

from scanapi.errors import BadConfigurationError


class StringEvaluator:
    variable_pattern = re.compile(
        r"(?P<something_before>\w*)(?P<start>\${)(?P<variable>\w*)(?P<end>})(?P<something_after>\w*)"
    )  # ${<variable>}

    @classmethod
    def evaluate(cls, sequence):
        try:
            return cls._evaluate_env_var(sequence)
        except BadConfigurationError as e:
            logger.error(e)
            sys.exit()

    @classmethod
    def _evaluate_env_var(cls, sequence):
        matches = cls.variable_pattern.finditer(sequence)

        if not matches:
            return sequence

        for match in matches:
            variable_name = match.group("variable")

            if any(letter.islower() for letter in variable_name):
                continue

            try:
                variable_value = os.environ[variable_name]
            except KeyError as e:
                raise BadConfigurationError(e)

            sequence = cls._replace_var_with_value(
                sequence, match.group(), variable_value
            )

        return sequence

    @classmethod
    def _replace_var_with_value(cls, sequence, variable, variable_value):
        variable = re.escape(variable)
        return re.sub(variable, variable_value, sequence)

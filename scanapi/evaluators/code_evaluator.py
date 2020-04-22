import logging
import re

from scanapi.errors import InvalidPythonCodeError

logger = logging.getLogger(__name__)


class CodeEvaluator:
    python_code_pattern = re.compile(
        r"(?P<something_before>\w*)(?P<start>\${{)(?P<python_code>.*)(?P<end>}})(?P<something_after>\w*)"
    )  # ${{<python_code>}}

    @classmethod
    def evaluate(cls, sequence, vars):
        # To avoid circular imports
        from scanapi.evaluators.string_evaluator import StringEvaluator

        # Available imports to be used dinamically in the API spec
        import datetime
        import math
        import random
        import time
        import uuid

        match = cls.python_code_pattern.search(sequence)

        if not match:
            return sequence

        code = match.group("python_code")

        try:
            response = vars.get("response")
            python_code_value = str(eval(code))
            return StringEvaluator.replace_var_with_value(
                sequence, match.group(), python_code_value
            )
        except Exception as e:
            raise InvalidPythonCodeError(str(e))

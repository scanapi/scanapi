import logging
import re
from types import SimpleNamespace

from scanapi.errors import InvalidPythonCodeError


logger = logging.getLogger(__name__)
python_code_pattern = re.compile(
    r"(?P<something_before>\w*)(?P<start>\${{)(?P<python_code>.*)(?P<end>}})(?P<something_after>\w*)"
)  # ${{<python_code>}}


class CodeEvaluator:
    def __init__(self, string_evaluator):
        self.string_evaluator = string_evaluator
        self.api_tree = string_evaluator.api_tree

    def evaluate(self, sequence):
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
            return self.string_evaluator.replace_var_with_value(
                sequence, match.group(), python_code_value
            )
        except Exception as e:
            raise InvalidPythonCodeError(str(e))

# Available imports to be used dinamically in the API spec
import datetime  # noqa: F401
import logging
import math  # noqa: F401
import random  # noqa: F401
import re
import time  # noqa: F401
import uuid  # noqa: F401

from scanapi.errors import InvalidPythonCodeError

logger = logging.getLogger(__name__)


class CodeEvaluator:
    python_code_pattern = re.compile(
        r"(?P<something_before>\w*)(?P<start>\${{)(?P<python_code>.*)(?P<end>}})(?P<something_after>\w*)"
    )  # ${{<python_code>}}

    @classmethod
    def evaluate(cls, sequence, vars, is_a_test_case=False):
        match = cls.python_code_pattern.search(str(sequence))

        if not match:
            return sequence

        code = match.group("python_code")
        response = vars.get("response")

        try:
            if is_a_test_case:
                return cls._assert_code(code, response)

            return cls._evaluate_sequence(sequence, match, code, response)
        except Exception as e:
            raise InvalidPythonCodeError(str(e), code)

    @classmethod
    def _assert_code(cls, code, response):
        """Assert a Python code statement

        :param code: python code that ScanAPI needs to assert
        :type code: string
        :param response: the response for the current request that is being tested
        :type response: requests.Response
        :return: A boolean that indicates if assert is True/False and, if False, the code tested.
        :rtype: (boolean, string)
        """
        try:
            assert eval(code)
            return (True, None)
        except AssertionError:
            return (False, code.strip())

    @classmethod
    def _evaluate_sequence(cls, sequence, match, code, response):
        # To avoid circular imports
        from scanapi.evaluators.string_evaluator import StringEvaluator

        return StringEvaluator.replace_var_with_value(
            sequence, match.group(), str(eval(code))
        )

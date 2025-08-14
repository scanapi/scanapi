# Available imports to be used dinamically in the API spec
import datetime  # noqa: F401
import math  # noqa: F401
import random  # noqa: F401
import re
import time  # noqa: F401
import uuid  # noqa: F401

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_globals, safe_builtins

from scanapi.errors import InvalidPythonCodeError


class CodeEvaluator:
    python_code_pattern = re.compile(
        r"(?P<something_before>\w*)"
        r"(?P<start>\${{)"
        r"(?P<python_code>.*)"
        r"(?P<end>}})"
        r"(?P<something_after>\w*)"
    )  # ${{<python_code>}}

    @classmethod
    def evaluate(cls, sequence, spec_vars, is_a_test_case=False):
        """Receives a sequence of characters and evaluates any python code
        present on it

        Args:
            sequence[string]: sequence of characters to be evaluated
            spec_vars[dict]: dictionary containing the SpecEvaluator variables
            is_a_test_case[bool]: indicator for checking if the given evaluation
            is a test case

        Returns:
            tuple: a tuple containing:
                -  [Boolean]: True if python statement is valid
                -  [string]: None if valid evaluation, tested code otherwise

        Raises:
            InvalidPythonCodeError: If receives invalid python statements
            (eg. 1/0)

        """
        match = cls.python_code_pattern.search(str(sequence))

        if not match:
            return sequence

        code = match.group("python_code")
        response = spec_vars.get("response")

        try:
            if is_a_test_case:
                return cls._assert_code(code, response)

            return cls._evaluate_sequence(sequence, match, code, response)
        except Exception as e:
            raise InvalidPythonCodeError(str(e), code)

    @classmethod
    def _get_safe_globals(cls, response=None):
        """Create a secure global context for code execution.

        Args:
            response: Optional response object for test assertions

        Returns:
            dict: Safe global context with restricted access
        """
        safe_context = safe_globals.copy()
        safe_context["__builtins__"] = safe_builtins.copy()

        # Add iterator functions for generator expressions and comprehensions
        safe_context["_iter_unpack_sequence_"] = iter
        safe_context["_getiter_"] = iter
        safe_context["_getattr_"] = getattr

        essential_builtins = {
            "all": all,
            "any": any,
            "len": len,
            "str": str,
        }
        safe_context["__builtins__"].update(essential_builtins)

        # Add allowed modules and functions
        allowed_modules = {
            "datetime": datetime,
            "math": math,
            "random": random,
            "re": re,
            "time": time,
            "uuid": uuid,
        }
        safe_context.update(allowed_modules)

        # Add response object if provided (for test assertions)
        if response is not None:
            safe_context["response"] = response

        return safe_context

    @classmethod
    def _safe_eval(cls, code, global_context=None):
        """Safely evaluate Python code using RestrictedPython with mode='eval'.

        Args:
            code[string]: Python code to evaluate
            global_context[dict]: Global context for evaluation

        Returns:
            Result of code evaluation

        Raises:
            InvalidPythonCodeError: If code compilation or execution fails
        """
        if global_context is None:
            global_context = cls._get_safe_globals()

        try:
            # Compile the code with restrictions using mode='eval'
            compiled_code = compile_restricted(code, "<string>", mode="eval")
            if compiled_code is None:
                raise InvalidPythonCodeError(
                    "Failed to compile restricted code", code
                )

            # Execute the compiled code securely
            result = eval(compiled_code, global_context)
            return result

        except SyntaxError as e:
            raise InvalidPythonCodeError(f"Syntax error in code: {e}", code)
        except Exception as e:
            raise InvalidPythonCodeError(str(e), code)

    @classmethod
    def _assert_code(cls, code, response):
        """Assert a Python code statement using RestrictedPython.

        The evaluation's global context is enriched with the response to support
        comprehensions using RestrictedPython for security.

        Args:
            code[string]: python code that ScanAPI needs to assert
            response[requests.Response]: the response for the current request
            that is being tested

        Returns:
            tuple: a tuple containing:
                -  [Boolean]: a boolean that indicates if assert
                is True/False
                -  [string]: None if valid evaluation, code tested otherwise

        Raises:
            AssertionError: If python statement evaluates False

        """
        global_context = cls._get_safe_globals(response)
        ok = cls._safe_eval(code, global_context)
        return ok, None if ok else code.strip()

    @classmethod
    def _evaluate_sequence(cls, sequence, match, code, response):
        # To avoid circular imports
        from scanapi.evaluators.string_evaluator import StringEvaluator

        global_context = cls._get_safe_globals(response)
        result = cls._safe_eval(code, global_context)

        return StringEvaluator.replace_var_with_value(
            sequence, match.group(), str(result)
        )

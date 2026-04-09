import re
from functools import singledispatch

from scanapi.evaluators.string_evaluator import StringEvaluator


class SpecEvaluator:
    """Evaluates spec variables by resolving references and substituting values.

    Acts as a registry of resolved variables for a given endpoint. Supports
    dict-like access, lazy resolution of endpoint-level vars, and filtering
    of response-dependent variables before execution.
    """

    def __init__(self, endpoint, spec_vars, extras=None, filter_responses=True):
        """Initialise the evaluator with an endpoint and its spec variables."""
        self.endpoint = endpoint
        self.registry = {}
        self.update(spec_vars, extras=extras, filter_responses=filter_responses)

    def evaluate(self, element):
        """Evaluate an element by resolving any variable references it contains.

        Dispatches to the appropriate evaluator based on the element type
        (str, dict, list, or passthrough for other types).
        """
        return evaluate(element, self)

    def evaluate_assertion(self, element):
        """Evaluate a string element as a test assertion.

        Similar to evaluate() but marks the evaluation as a test case,
        which affects how the StringEvaluator processes the expression.
        """
        return _evaluate_str(element, self, is_a_test_case=True)

    def update(self, spec_vars, extras=None, filter_responses=False):
        """Merge new variables into the registry after evaluating them."""
        if extras is None:
            extras = {}

        if filter_responses:
            spec_vars = self.filter_response_var(spec_vars)

        values = {
            key: evaluate(value, extras) for key, value in spec_vars.items()
        }
        self.registry.update(extras)
        self.registry.update(values)

    def get(self, key, default=None):
        """Return the value for key if it exists, otherwise default."""
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        """Return the string representation of the internal registry."""
        return self.registry.__repr__()

    def __getitem__(self, key):
        """Retrieve a variable by key. Falls back to endpoint-level vars."""
        if key in self:
            return self.registry[key]

        all_vars = self.endpoint.get_all_vars()
        if key in all_vars:
            return all_vars[key]

        raise KeyError(key)

    def __delitem__(self, key):
        """Remove a variable from the registry by key."""
        if key in self:
            del self.registry[key]
        else:
            raise KeyError(key)

    def __contains__(self, key):
        """Check whether key exists in the registry."""
        return key in self.registry

    def keys(self):
        """Returns a copy of the dictionary’s list of keys.
        Returns:
            [list]: list of keys.

        """
        return self.registry.keys()

    @classmethod
    def filter_response_var(cls, spec_vars):
        """Returns a copy of ``spec_vars`` without 'response' references.

        Any items with a ``response.*`` reference in their value are left out.

        Returns:
            [dict]: filtered dictionary.

        """
        pattern = re.compile(r"(?:(\s*response\.\w+))")
        return {k: v for k, v in spec_vars.items() if not pattern.search(v)}


@singledispatch
def evaluate(expression, spec_vars):
    """Evaluate an expression by resolving variable references.

    Uses single dispatch to handle different types: strings are passed
    through StringEvaluator, dicts and lists are evaluated recursively,
    and all other types are returned as-is.
    """
    return expression


@evaluate.register(str)
def _evaluate_str(element, spec_vars, is_a_test_case=False):
    """Evaluate a string expression, resolving variable references."""
    return StringEvaluator.evaluate(element, spec_vars, is_a_test_case)


@evaluate.register(dict)
def _evaluate_dict(element, spec_vars):
    """Recursively evaluate all values in a dictionary."""
    return {key: evaluate(value, spec_vars) for key, value in element.items()}


@evaluate.register(list)
@evaluate.register(tuple)
def _evaluate_collection(elements, spec_vars):
    """Recursively evaluate all items in a list or tuple."""
    return [evaluate(item, spec_vars) for item in elements]

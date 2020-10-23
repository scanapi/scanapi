import logging
import re
from functools import singledispatch

from scanapi.evaluators.string_evaluator import StringEvaluator

logger = logging.getLogger(__name__)


class SpecEvaluator:
    def __init__(self, endpoint, vars_, extras=None, filter_responses=True):
        self.endpoint = endpoint
        self.registry = {}
        self.update(vars_, extras=extras, filter_responses=filter_responses)

    def evaluate(self, element):
        return evaluate(element, self)

    def evaluate_assertion(self, element):
        return _evaluate_str(element, self, is_a_test_case=True)

    def update(self, vars, extras=None, filter_responses=False):
        if extras is None:
            extras = {}

        if filter_responses:
            vars = self.filter_response_var(vars)

        values = {key: evaluate(value, extras) for key, value in vars.items()}
        self.registry.update(extras)
        self.registry.update(values)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        return self.registry.__repr__()

    def keys(self):
        return self.registry.keys()

    def __getitem__(self, key):
        if key in self:
            return self.registry[key]

        if key in self.endpoint.parent.vars:
            return self.endpoint.parent.vars[key]

        raise KeyError(key)

    def __delitem__(self, key):
        if key in self:
            del self.registry[key]
        else:
            raise KeyError(key)

    def __contains__(self, key):
        return key in self.registry

    def keys(self):
        """Returns a copy of the dictionary’s list of keys.
        Returns:
            [list]: list of keys.

        """
        return self.registry.keys()

    @classmethod
    def filter_response_var(cls, vars_):
        """Returns a dictionary without vars that evaluate response.
        Returns:
            [dict]: filtered dictionary.

        """
        pattern = re.compile(r"(?:(\s*response\.\w+))")
        return {k: v for k, v in vars_.items() if not pattern.search(v)}


@singledispatch
def evaluate(expression, vars):
    return expression


@evaluate.register(str)
def _evaluate_str(element, vars, is_a_test_case=False):
    return StringEvaluator.evaluate(element, vars, is_a_test_case)


@evaluate.register(dict)
def _evaluate_dict(element, vars):
    return {key: evaluate(value, vars) for key, value in element.items()}


@evaluate.register(list)
@evaluate.register(tuple)
def _evaluate_collection(elements, vars):
    return [evaluate(item, vars) for item in elements]

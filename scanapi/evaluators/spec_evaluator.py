import logging
from functools import singledispatch

from scanapi.evaluators.string_evaluator import StringEvaluator

logger = logging.getLogger(__name__)


class SpecEvaluator:
    def __init__(self, endpoint, vars={}):
        self.endpoint = endpoint
        self.registry = {}
        self.update(vars)

    def evaluate(self, element):
        return evaluate(element, self)

    def evaluate_assertion(self, element):
        return _evaluate_str(element, self, is_a_test_case=True)

    def update(self, vars, extras=None, preevaluate=False):
        if preevaluate:
            values = {
                key: evaluate(value, extras) for key, value in vars.items()
            }
            self.registry.update(values)
            self.registry.update(extras)
        else:
            self.registry.update(vars)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        return self.registry.__repr__()

    def __getitem__(self, key):
        if key in self:
            return self.registry[key]

        if key in self.endpoint.parent.vars:
            return self.endpoint.parent.vars[key]

        raise KeyError(key)

    def __contains__(self, key):
        return key in self.registry


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

import logging

from scanapi.refactor.evaluators.string_evaluator import StringEvaluator

logger = logging.getLogger(__name__)


class SpecEvaluator:
    @classmethod
    def evaluate(cls, element):
        if isinstance(element, dict):
            return cls._evaluate_dict(element)

        if isinstance(element, list):
            return cls._evaluate_list(element)

        if not isinstance(element, str):
            return element

        return StringEvaluator.evaluate(element)

    @classmethod
    def _evaluate_dict(cls, element):
        evaluated_dict = {}
        for key, value in element.items():
            evaluated_dict[key] = cls.evaluate(value)

        return evaluated_dict

    @classmethod
    def _evaluate_list(cls, elements):
        evaluated_list = []
        for item in elements:
            evaluated_list.append(cls.evaluate(item))

        return evaluated_list

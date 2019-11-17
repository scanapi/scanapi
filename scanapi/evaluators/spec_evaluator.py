import logging

from scanapi.evaluators.string_evaluator import StringEvaluator

logger = logging.getLogger(__name__)


class SpecEvaluator:
    def __init__(self, api_tree):
        self.api_tree = api_tree
        self.string_evaluator = StringEvaluator(self)

    def evaluate(self, element):
        if isinstance(element, dict):
            return self.evaluate_dict(element)

        if isinstance(element, list):
            return self.evaluate_list(element)

        if not isinstance(element, str):
            return element

        return self.string_evaluator.evaluate(element)

    def evaluate_dict(self, element):
        evaluated_dict = {}
        for key, value in element.items():
            evaluated_dict[key] = self.evaluate(value)

        return evaluated_dict

    def evaluate_list(self, elements):
        evaluated_list = []
        for item in elements:
            evaluated_list.append(self.evaluate(item))

        return evaluated_list

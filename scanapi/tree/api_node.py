from abc import ABC, abstractmethod
from scanapi.errors import InvalidKeyError


class APINode(ABC):
    def __init__(self, api_tree, node_spec):
        self.api_tree = api_tree
        self.spec_evaluator = api_tree.spec_evaluator
        self.spec = node_spec
        self.validate()

    @abstractmethod
    def validate(self):
        pass

    @classmethod
    def validate_keys(self, keys, available_keys, scope):
        for key in keys:
            if not key in available_keys:
                raise InvalidKeyError(key, scope, available_keys)

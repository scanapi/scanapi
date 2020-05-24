import logging
import requests

from scanapi.tree.tree_keys import NAME_KEY, ASSERT_KEY
from scanapi.utils import validate_keys

logger = logging.getLogger(__name__)


class TestingNode:
    __test__ = False
    SCOPE = "test"
    ALLOWED_KEYS = (ASSERT_KEY, NAME_KEY)
    REQUIRED_KEYS = (NAME_KEY, ASSERT_KEY)

    def __init__(self, spec, request):
        self.spec = spec
        self.request = request
        self._validate()

    def __getitem__(self, item):
        return self.spec[item]

    @property
    def name(self):
        return self["name"]

    @property
    def assertion(self):
        return self["assert"]

    @property
    def full_name(self):
        return f"{self.request.endpoint.name}::{self.request.name}::{self.name}"

    def run(self):
        passed, error = self.request.endpoint.vars.evaluate_assertion(self.assertion)
        self._log_result(passed, error)

    def _log_result(self, passed, error):
        passed = "PASSED" if passed else "FAILED"
        logger.info("\a [%s] %s", passed, self.full_name)
        if error:
            logger.info("\t  %s is false", error)

    def _validate(self):
        validate_keys(
            self.spec.keys(), self.ALLOWED_KEYS, self.REQUIRED_KEYS, self.SCOPE
        )

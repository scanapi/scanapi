import logging

from scanapi.session import session
from scanapi.test_status import TestStatus
from scanapi.tree.tree_keys import ASSERT_KEY, NAME_KEY
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
        return self[NAME_KEY]

    @property
    def assertion(self):
        return self[ASSERT_KEY]

    @property
    def full_name(self):
        return f"{self.request.endpoint.name}::{self.request.name}::{self.name}"

    def run(self):
        try:
            passed, failure = self.request.endpoint.vars.evaluate_assertion(
                self.assertion
            )

            status = TestStatus.PASSED if passed else TestStatus.FAILED
            error = None
        except Exception as e:
            status = TestStatus.ERROR
            failure = None
            error = str(e)

        self._process_result(status)
        self._log_result(status, failure)

        return {
            "name": self.full_name,
            "status": status,
            "failure": failure,
            "error": error,
        }

    def _process_result(self, status):
        if status == TestStatus.ERROR:
            session.increment_errors()
            return

        if status == TestStatus.FAILED:
            session.increment_failures()
            return

        if status == TestStatus.PASSED:
            session.increment_successes()

    def _log_result(self, status, failure):
        logger.debug("\a [%s] %s", status.upper(), self.full_name)
        if failure:
            logger.debug("\t  %s is false", failure)

    def _validate(self):
        validate_keys(
            self.spec.keys(), self.ALLOWED_KEYS, self.REQUIRED_KEYS, self.SCOPE
        )

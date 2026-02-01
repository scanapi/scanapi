from scanapi.session import session
from scanapi.test_status import TestStatus
from scanapi.tree.tree_keys import ASSERT_KEY, NAME_KEY
from scanapi.utils import validate_keys


class TestingNode:
    """Represents a test node defined in the ScanAPI specification.

    A TestingNode validates a test definition, executing its assertion
    against the evaluated API response, and reporting the result status.
    """

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
        """Run the test assertion and return its result.

        This method evaluates the assertion defined in the test,
        updates the global session counters based on the outcome,
        and returns a dictionary describing the test execution.

        Returns:
            dict: A dictionary containing:
                - name (str): Full hierarchical name of the test.
                - status (TestStatus): Result of the test execution.
                - failure (any): Assertion failure details, if available.
                - error (str): Error message if an exception was raised.
        """

        try:
            (
                passed,
                failure,
            ) = self.request.endpoint.spec_vars.evaluate_assertion(
                self.assertion
            )

            status = TestStatus.PASSED if passed else TestStatus.FAILED
            error = None
        except Exception as e:
            status = TestStatus.ERROR
            failure = None
            error = str(e)

        self._process_result(status)

        return {
            "name": self.full_name,
            "status": status,
            "failure": failure,
            "error": error,
        }

    @staticmethod
    def _process_result(status):
        """Increment the number of session errors/failures/successes
        depending on the test status.

        Args:
            status [string]: the status of the test: passed, failed or error.
        """
        if status == TestStatus.ERROR:
            session.increment_errors()
            return

        if status == TestStatus.FAILED:
            session.increment_failures()
            return

        if status == TestStatus.PASSED:
            session.increment_successes()

    def _validate(self):
        validate_keys(
            self.spec.keys(), self.ALLOWED_KEYS, self.REQUIRED_KEYS, self.SCOPE
        )

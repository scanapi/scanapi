import sys
from datetime import datetime

from scanapi.exit_code import ExitCode


class Session:
    """ Class that handles each scanapi session. """

    def __init__(self):
        """ Constructs a Session object. """
        self.successes = 0
        self.failures = 0
        self.errors = 0
        self.exit_code = ExitCode.OK
        self.started_at = datetime.now()

    @property
    def succeed(self):
        """ Property decorated method that returns success (no errors or failures. """
        return self.errors == 0 and self.failures == 0

    def exit(self):
        """ Handles the exiting of the Session """
        if self.errors:
            sys.exit(ExitCode.TESTS_ERROR)

        if self.failures:
            sys.exit(ExitCode.TESTS_FAILED)

        sys.exit(self.exit_code)

    def increment_successes(self):
        """ Increments success count. """
        self.successes += 1

    def increment_failures(self):
        """ Increments failure count. """
        self.failures += 1

    def increment_errors(self):
        """ Increments error count. """
        self.errors += 1

    def elapsed_time(self):
        """ Returns the delta of time since session object started. """
        return datetime.now() - self.started_at


session = Session()

import sys

from datetime import datetime

from scanapi.exit_code import ExitCode


class Session:
    def __init__(self):
        self.successes = 0
        self.failures = 0
        self.errors = 0
        self.exit_code = ExitCode.OK

    @property
    def succeed(self):
        return self.errors == 0 and self.failures == 0

    def start(self):
        self.started_at = datetime.now()

    def exit(self):
        if self.errors:
            sys.exit(ExitCode.TESTS_ERROR)

        if self.failures:
            sys.exit(ExitCode.TESTS_FAILED)

        sys.exit(self.exit_code)

    def increment_successes(self):
        self.successes += 1

    def increment_failures(self):
        self.failures += 1

    def increment_errors(self):
        self.errors += 1

    def elapsed_time(self):
        return datetime.now() - self.started_at


session = Session()

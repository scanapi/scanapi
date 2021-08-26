"""Code based on solution: https://github.com/pytest-dev/pytest/blob/\
83891d9022076375cede03bfd8c932d450e6fcf8/src/_pytest/config/__init__.py#L67"""

import enum


class ExitCode(enum.IntEnum):
    """Encodes the valid exit codes by ScanAPI."""

    #: tests passed
    OK = 0
    #: tests failed
    TESTS_FAILED = 1
    #: tests error
    TESTS_ERROR = 2
    #: Error while trying to make a request
    REQUEST_ERROR = 3
    #: ScanAPI was misused
    USAGE_ERROR = 4
    #: an internal error got in the way
    INTERNAL_ERROR = 5

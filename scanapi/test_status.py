class TestStatus:
    """ Class that holds test statuses - passed, failed or error. """

    __test__ = False
    """
    Encodes the valid test status.
    """

    #: test passed
    PASSED = "passed"
    #: test failed
    FAILED = "failed"
    #: test error
    ERROR = "error"

from random import randrange

from pytest import mark, raises

from scanapi.session import Session


@mark.describe("session")
@mark.describe("__init__")
class TestInit:
    def test_init_successes_and_failures(self):
        session = Session()

        assert session.successes == 0
        assert session.failures == 0


@mark.describe("session")
@mark.describe("succeed")
class TestSucceed:
    @mark.parametrize(
        "failures, errors, expected",
        [(0, 0, True), (1, 0, False), (0, 1, False), (2, 1, False)],
    )
    @mark.it(
        "should fail when there is a failure and should succeed when there is no failure"
    )
    def test_failed_when_there_is_failure(self, failures, errors, expected):
        session = Session()
        session.failures = failures
        session.errors = errors
        assert session.succeed == expected


@mark.describe("session")
@mark.describe("start")
class TestStart:
    @mark.it("should initialize started_at with current time")
    @mark.freeze_time("2020-06-15 18:54:57")
    def test_init_started_at(self):
        session = Session()

        assert str(session.started_at) == "2020-06-15 18:54:57"


@mark.describe("session")
@mark.describe("exit")
class TestExit:
    @mark.it("should exit with proper error")
    @mark.parametrize(
        "failures, errors, error_code",
        [(0, 0, 0), (1, 0, 1), (0, 1, 2), (1, 1, 2)],
    )
    def test_exit_with_proper_error(self, failures, errors, error_code):
        session = Session()
        session.failures = failures
        session.errors = errors
        with raises(SystemExit) as excinfo:
            session.exit()

        assert excinfo.type == SystemExit
        assert excinfo.value.code == error_code


@mark.describe("session")
@mark.describe("increment_successes")
class TestIncrementSuccesses:
    @mark.it("should increment successes")
    def test_increment(self):
        session = Session()
        times = randrange(1, 10)

        for _ in range(times):
            session.increment_successes()

        assert session.successes == times


@mark.describe("session")
@mark.describe("increment_failures")
class TestIncrementFailures:
    @mark.it("should increment failures")
    def test_increment(self):
        session = Session()
        times = randrange(1, 10)

        for _ in range(times):
            session.increment_failures()

        assert session.failures == times


@mark.describe("session")
@mark.describe("increment_errors")
class TestIncrementErrors:
    @mark.it("should increment error")
    def test_increment(self):
        session = Session()
        times = randrange(1, 10)

        for _ in range(times):
            session.increment_errors()

        assert session.errors == times


@mark.describe("session")
@mark.describe("elapsed_time")
class TestElapsedTime:
    @mark.it("should return time")
    @mark.freeze_time("2020-06-15 18:54:57")
    def test_return_time(self, freezer):
        session = Session()

        freezer.move_to("2020-06-15 18:56:38")

        assert str(session.elapsed_time()) == "0:01:41"

import pytest

from random import randrange

from scanapi.session import Session


class TestSession:
    class TestInit:
        def test_init_successes_and_failures(self):
            session = Session()

            assert session.successes == 0
            assert session.failures == 0

    class TestSucceed:
        @pytest.mark.parametrize(
            "failures, errors, expected",
            [(0, 0, True), (1, 0, False), (0, 1, False), (2, 1, False)],
        )
        def test_failed_when_there_is_failure(self, failures, errors, expected):
            session = Session()
            session.failures = failures
            session.errors = errors
            assert session.succeed == expected

    class TestStart:
        @pytest.mark.freeze_time("2020-06-15 18:54:57")
        def test_init_started_at(self):
            session = Session()
            session.start()

            assert str(session.started_at) == "2020-06-15 18:54:57"

    class TestExit:
        @pytest.mark.parametrize(
            "failures, errors, error_code",
            [(0, 0, 0), (1, 0, 1), (0, 1, 2), (1, 1, 2)],
        )
        def test_exit_with_proper_error(self, failures, errors, error_code):
            session = Session()
            session.failures = failures
            session.errors = errors
            with pytest.raises(SystemExit) as excinfo:
                session.exit()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == error_code

    class TestIncrementSuccesses:
        def test_increment(self):
            session = Session()
            times = randrange(1, 10)

            for _ in range(times):
                session.increment_successes()

            assert session.successes == times

    class TestIncrementFailures:
        def test_increment(self):
            session = Session()
            times = randrange(1, 10)

            for _ in range(times):
                session.increment_failures()

            assert session.failures == times

    class TestIncrementErrors:
        def test_increment(self):
            session = Session()
            times = randrange(1, 10)

            for _ in range(times):
                session.increment_errors()

            assert session.errors == times

    class TestElapsedTime:
        @pytest.mark.freeze_time("2020-06-15 18:54:57")
        def test_return_time(self, freezer):
            session = Session()
            session.start()

            freezer.move_to("2020-06-15 18:56:38")

            assert str(session.elapsed_time()) == "0:01:41"

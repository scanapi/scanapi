import pytest

from random import randrange

from scanapi.session import Session


class TestSession:
    class TestInit:
        def test_init_successes_and_failures(self):
            session = Session()

            assert session.successes == 0
            assert session.failures == 0

    class TestFailed:
        @pytest.mark.parametrize(
            "failures, expected", [(0, False), (1, True), (2, True)]
        )
        def test_failed_when_there_is_failure(self, failures, expected):
            session = Session()
            session.failures = failures
            assert session.failed == expected

    class TestStart:
        @pytest.mark.freeze_time("2020-06-15 18:54:57")
        def test_init_started_at(self):
            session = Session()
            session.start()

            assert str(session.started_at) == "2020-06-15 18:54:57"

    class TestIncrementSuccesses:
        def test_increment(self):
            session = Session()
            times = randrange(1, 100)

            for _ in range(times):
                session.increment_successes()

            assert session.successes == times

    class TestIncrementFailures:
        def test_increment(self):
            session = Session()
            times = randrange(1, 100)

            for _ in range(times):
                session.increment_failures()

            assert session.failures == times

    class TestElapsedTime:
        @pytest.mark.freeze_time("2020-06-15 18:54:57")
        def test_return_time(self, freezer):
            session = Session()
            session.start()

            freezer.move_to("2020-06-15 18:56:38")

            assert str(session.elapsed_time()) == "0:01:41"

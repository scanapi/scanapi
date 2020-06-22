import logging
import pytest

from scanapi.errors import MissingMandatoryKeyError
from scanapi.tree import EndpointNode, RequestNode, TestingNode

log = logging.getLogger(__name__)


class TestTestingNode:
    class TestInit:
        def test_missing_required_keys(self):
            with pytest.raises(MissingMandatoryKeyError) as excinfo:
                request_node = RequestNode(
                    spec={"name": "foo", "path": "bar"},
                    endpoint=EndpointNode({"name": "foo", "requests": [{}]}),
                )
                test_node = TestingNode(spec={}, request=request_node)

            assert (
                str(excinfo.value) == "Missing 'assert', 'name' key(s) at 'test' scope"
            )

    class TestFullName:
        def test_full_name(self):
            endpoint_node = EndpointNode({"name": "foo"})
            request_node = RequestNode(spec={"name": "bar"}, endpoint=endpoint_node)
            test_node = TestingNode(
                spec={"name": "lol", "assert": "okay"}, request=request_node
            )

            assert test_node.full_name == "foo::bar::lol"

    class TestRun:
        @pytest.fixture
        def testing_node(self):
            __test__ = False
            endpoint_node = EndpointNode(spec={"name": "foo"})
            request_node = RequestNode(spec={"name": "bar"}, endpoint=endpoint_node)
            spec = {
                "name": "status_is_200",
                "assert": "${{ response.status_code == 200 }}",
            }
            return TestingNode(spec=spec, request=request_node)

        @pytest.fixture
        def mock_evaluate(self, mocker):
            return mocker.patch(
                "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate_assertion"
            )

        @pytest.fixture
        def mock_increment_successes(self, mocker):
            return mocker.patch("scanapi.tree.testing_node.session.increment_successes")

        @pytest.fixture
        def mock_increment_failures(self, mocker):
            return mocker.patch("scanapi.tree.testing_node.session.increment_failures")

        class TestWhenTestPassed:
            def test_build_result(
                self, mock_evaluate, testing_node,
            ):
                mock_evaluate.return_value = (True, None)

                result = testing_node.run()
                assert result == {
                    "name": "foo::bar::status_is_200",
                    "status": "passed",
                    "failure": None,
                    "error": None,
                }

            def test_increment_successes(
                self,
                mock_evaluate,
                mock_increment_successes,
                mock_increment_failures,
                testing_node,
            ):
                mock_evaluate.return_value = (True, None)

                testing_node.run()
                assert mock_increment_successes.call_count == 1
                assert not mock_increment_failures.called

            def test_logs_test_results(self, mock_evaluate, caplog, testing_node):
                mock_evaluate.return_value = (True, None)

                with caplog.at_level(logging.DEBUG):
                    testing_node.run()
                assert "\x07 [PASSED] foo::bar::status_is_200" in caplog.text

        class TestWhenTestFailed:
            def test_build_result(
                self, mock_evaluate, testing_node,
            ):
                mock_evaluate.return_value = (False, "response.status_code == 200")

                result = testing_node.run()
                assert result == {
                    "name": "foo::bar::status_is_200",
                    "status": "failed",
                    "failure": "response.status_code == 200",
                    "error": None,
                }

            def test_increment_failures(
                self,
                mock_evaluate,
                mock_increment_successes,
                mock_increment_failures,
                testing_node,
            ):
                mock_evaluate.return_value = (False, "response.status_code == 200")

                testing_node.run()
                assert mock_increment_failures.call_count == 1
                assert not mock_increment_successes.called

            def test_logs_test_results(self, mock_evaluate, caplog, testing_node):
                mock_evaluate.return_value = (False, "response.status_code == 200")

                with caplog.at_level(logging.DEBUG):
                    testing_node.run()

                assert "\x07 [FAILED] foo::bar::status_is_200" in caplog.text
                assert "\t  response.status_code == 200 is false" in caplog.text

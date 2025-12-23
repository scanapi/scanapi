from pytest import fixture, mark

from scanapi.tree import EndpointNode, RequestNode, TestingNode


@mark.describe("testing node")
@mark.describe("run")
class TestRun:
    @fixture
    def testing_node(self):
        endpoint_node = EndpointNode(spec={"name": "foo"})
        request_node = RequestNode(spec={"name": "bar"}, endpoint=endpoint_node)
        spec = {
            "name": "status_is_200",
            "assert": "${{ response.status_code == 200 }}",
        }
        return TestingNode(spec=spec, request=request_node)

    @fixture
    def mock_evaluate(self, mocker):
        return mocker.patch(
            "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate_assertion"
        )

    @fixture
    def mock_increment_successes(self, mocker):
        return mocker.patch(
            "scanapi.tree.testing_node.session.increment_successes"
        )

    @fixture
    def mock_increment_failures(self, mocker):
        return mocker.patch(
            "scanapi.tree.testing_node.session.increment_failures"
        )

    @mark.context("when test passed")
    @mark.it("should build result object")
    def test_build_result(
        self,
        mock_evaluate,
        testing_node,
    ):
        mock_evaluate.return_value = (True, None)

        result = testing_node.run()
        assert result == {
            "name": "foo::bar::status_is_200",
            "status": "passed",
            "failure": None,
            "error": None,
        }

    @mark.context("when test passed")
    @mark.it("should increment successes")
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

    @mark.context("when test failed")
    @mark.it("should build result object")
    def test_build_result_2(
        self,
        mock_evaluate,
        testing_node,
    ):
        mock_evaluate.return_value = (
            False,
            "response.status_code == 200",
        )

        result = testing_node.run()
        assert result == {
            "name": "foo::bar::status_is_200",
            "status": "failed",
            "failure": "response.status_code == 200",
            "error": None,
        }

    @mark.context("when test failed")
    @mark.it("should increment failures")
    def test_increment_failures(
        self,
        mock_evaluate,
        mock_increment_successes,
        mock_increment_failures,
        testing_node,
    ):
        mock_evaluate.return_value = (
            False,
            "response.status_code == 200",
        )

        testing_node.run()
        assert mock_increment_failures.call_count == 1
        assert not mock_increment_successes.called

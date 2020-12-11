import pytest

from scanapi.evaluators.spec_evaluator import SpecEvaluator
from scanapi.tree import EndpointNode


@pytest.mark.describe("Test Spec Evaluator")
class TestSpecEvaluator:
    @pytest.fixture
    def mock_string_evaluate(self, mocker):
        return mocker.patch(
            "scanapi.evaluators.spec_evaluator.StringEvaluator.evaluate"
        )

    @pytest.fixture
    def spec_evaluator(self):
        parent = EndpointNode({"name": "bar", "requests": [{}]})
        endpoint = EndpointNode({"name": "foo", "requests": [{}]}, parent)
        return SpecEvaluator(endpoint, {"name": "foo"})

    @pytest.mark.describe("Test Evaluate String")
    class TestEvaluateString:
        @pytest.mark.it("should call evaluate string")
        def test_should_call_evaluate_string(
            self, spec_evaluator, mock_string_evaluate
        ):
            string = "foo"
            spec_evaluator.evaluate(string)
            assert mock_string_evaluate.called_once_with(string)

        @pytest.mark.it("should call evaluate assertion string")
        def test_should_call_evaluate_assertion_string(
            self, spec_evaluator, mock_string_evaluate
        ):
            string = "foo"
            spec_evaluator.evaluate_assertion(string)
            assert mock_string_evaluate.called_once_with(string)

    @pytest.mark.describe("Test Evaluate Dict")
    class TestEvaluateDict:
        @pytest.mark.context("When Dict Is Empty")
        class TestWhenDictIsEmpty:
            @pytest.mark.it("return empty dict")
            def test_return_empty_dict(self, spec_evaluator):
                evaluated_dict = spec_evaluator.evaluate({})
                assert len(evaluated_dict) == 0

        @pytest.mark.context("When Dict Is Not Empty")
        class TestWhenDictIsNotEmpty:
            @pytest.mark.it("return evaluated dict")
            def test_return_evaluated_dict(
                self, spec_evaluator, mocker, mock_string_evaluate
            ):
                mock_string_evaluate.side_effect = ["foo", "bar"]
                assert spec_evaluator.evaluate(
                    {"app_id": "foo", "token": "bar",}
                ) == {"app_id": "foo", "token": "bar",}

                mock_string_evaluate.assert_has_calls(
                    [
                        mocker.call("foo", spec_evaluator, False),
                        mocker.call("bar", spec_evaluator, False),
                    ]
                )

    @pytest.mark.describe("Test Evaluate List")
    class TestEvaluateList:
        @pytest.mark.context("When List Is Empty")
        class TestWhenListIsEmpty:
            @pytest.mark.it("should return empty list")
            def test_return_empty_list(self, spec_evaluator):
                evaluated_list = spec_evaluator.evaluate([])
                assert len(evaluated_list) == 0

        @pytest.mark.context("When List Is Not Empty")
        class TestWhenListIsNotEmpty:
            @pytest.mark.it("should return evaluated list")
            def test_return_evaluated_list(
                self, spec_evaluator, mocker, mock_string_evaluate
            ):
                values = ["foo", "bar"]
                mock_string_evaluate.side_effect = values
                assert spec_evaluator.evaluate(values) == ["foo", "bar"]

                mock_string_evaluate.assert_has_calls(
                    [
                        mocker.call("foo", spec_evaluator, False),
                        mocker.call("bar", spec_evaluator, False),
                    ]
                )

    @pytest.mark.describe("Spec Evaluator Get Key")
    class TestSpecEvaluatorGetKey:
        @pytest.mark.it("should return none")
        def test_should_return_none(self, spec_evaluator):
            key = "some_key"
            value = spec_evaluator.get(key)
            assert value is None

        @pytest.mark.it("should return foo")
        def test_should_return_foo(self, spec_evaluator):
            key = "name"
            value = spec_evaluator.get(key)
            assert value == "foo"

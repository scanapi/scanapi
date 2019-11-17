import os
import pytest

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.evaluators.spec_evaluator import SpecEvaluator


class TestSpecEvaluator:
    @pytest.fixture
    def spec_evaluator(self):
        return SpecEvaluator({})

    class TestEvaluate:
        @pytest.fixture
        def mock_evaluate_dict(self, mocker):
            return mocker.patch(
                "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate_dict"
            )

        @pytest.fixture
        def mock_evaluate_list(self, mocker):
            return mocker.patch(
                "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate_list"
            )

        @pytest.fixture
        def mock_evaluate_string(self, mocker):
            return mocker.patch(
                "scanapi.evaluators.string_evaluator.StringEvaluator.evaluate"
            )

        class TestWhenElementIsDict:
            def test_should_call_evaluate_dict(
                self,
                spec_evaluator,
                mock_evaluate_dict,
                mock_evaluate_list,
                mock_evaluate_string,
            ):
                spec_evaluator.evaluate({})
                assert mock_evaluate_dict.called_once
                assert not mock_evaluate_list.called
                assert not mock_evaluate_string.called

        class TestWhenElementIsList:
            def test_should_call_evaluate_dict(
                self,
                spec_evaluator,
                mock_evaluate_dict,
                mock_evaluate_list,
                mock_evaluate_string,
            ):
                spec_evaluator.evaluate([])
                assert mock_evaluate_list.called_once
                assert not mock_evaluate_dict.called
                assert not mock_evaluate_string.called

        class TestWhenElementIsString:
            def test_should_call_evaluate_dict(
                self,
                spec_evaluator,
                mock_evaluate_dict,
                mock_evaluate_list,
                mock_evaluate_string,
            ):
                spec_evaluator.evaluate("")
                assert mock_evaluate_string.called_once
                assert not mock_evaluate_dict.called
                assert not mock_evaluate_list.called

    class TestEvaluateDict:
        class TestWhenDictIsEmpty:
            def test_return_empty_dict(self, spec_evaluator):
                evaluated_dict = spec_evaluator.evaluate_dict({})
                assert len(evaluated_dict) == 0

        class TestWhenDictIsNotEmpty:
            def test_return_evaluated_dict(self, mocker, spec_evaluator):
                mock_evaluate = mocker.patch(
                    "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate"
                )
                mock_evaluate.return_value = "evaluated_value"
                evaluated_dict = spec_evaluator.evaluate_dict(
                    {"token": "${API_TOKEN}", "app_id": "${APP_ID}"}
                )
                assert evaluated_dict == {
                    "app_id": "evaluated_value",
                    "token": "evaluated_value",
                }

    class TestEvaluateList:
        class TestWhenListIsEmpty:
            def test_return_empty_list(self, spec_evaluator):
                evaluated_list = spec_evaluator.evaluate_list([])
                assert len(evaluated_list) == 0

        class TestWhenListIsNotEmpty:
            def test_return_evaluated_list(self, mocker, spec_evaluator):
                mock_evaluate = mocker.patch(
                    "scanapi.evaluators.spec_evaluator.SpecEvaluator.evaluate"
                )
                mock_evaluate.return_value = "evaluated_value"
                evaluated_list = spec_evaluator.evaluate_list(
                    ["${API_TOKEN}", "${APP_ID}"]
                )
                assert evaluated_list == ["evaluated_value", "evaluated_value"]

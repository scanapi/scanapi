import os
import pytest

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.evaluators.spec_evaluator import SpecEvaluator
from scanapi.evaluators.string_evaluator import StringEvaluator
from scanapi.evaluators.code_evaluator import CodeEvaluator


class TestCodeEvaluator:
    @pytest.fixture
    def spec_evaluator(self):
        return SpecEvaluator({})

    @pytest.fixture
    def string_evaluator(self, spec_evaluator):
        return StringEvaluator(spec_evaluator)

    @pytest.fixture
    def code_evaluator(self, string_evaluator):
        return CodeEvaluator(string_evaluator)

    class TestEvaluate:
        @pytest.fixture
        def spec_evaluator(self):
            class APITreeMock:
                def __init__(self):
                    self.responses = {}

            return SpecEvaluator(APITreeMock())

        class TestWhenDoesNotMatchThePattern:
            test_data = ["no code", "${CODE}", "${code}", "{{code}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, code_evaluator, sequence):
                assert code_evaluator.evaluate(sequence) == sequence

        class TestWhenMatchesThePattern:
            test_data = [("${{1 + 1}}", "2"), ("${{'hi'*4}}", "hihihihi")]

            @pytest.mark.parametrize("sequence, expected", test_data)
            def test_should_return_evaluated_code(
                self, code_evaluator, sequence, expected
            ):
                assert code_evaluator.evaluate(sequence) == expected

            class TestWhenCodeContainsPreSavedRequest:
                @pytest.fixture
                def spec_evaluator(self):
                    class MockResponse:
                        def json(self):
                            return [{"id": 1, "name": "John"}]

                    class APITreeMock:
                        def __init__(self):
                            self.responses = {"user_details": MockResponse()}

                    return SpecEvaluator(APITreeMock())

                test_data = [
                    ("${{responses.user_details.json()[0]['id']}}", "1"),
                    ("${{responses.user_details.json()[0]['name']}}", "John"),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_response(
                    self, code_evaluator, mocker, sequence, expected
                ):
                    assert code_evaluator.evaluate(sequence) == expected

            class TestWhenCodeBreaks:
                def test_should_raises_invalid_python_code_error(self, code_evaluator):
                    with pytest.raises(InvalidPythonCodeError) as excinfo:
                        code_evaluator.evaluate("${{1/0}}")

                    assert (
                        str(excinfo.value)
                        == "Invalid Python code defined in the API spec: division by zero"
                    )

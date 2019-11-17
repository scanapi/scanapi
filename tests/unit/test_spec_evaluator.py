import os
import pytest

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.spec_evaluator import SpecEvaluator


class TestSpecEvaluator:
    @pytest.fixture
    def spec_evaluator(self):
        return SpecEvaluator({})

    class TestEvaluate:
        @pytest.fixture
        def mock_evaluate_dict(self, mocker):
            return mocker.patch("scanapi.spec_evaluator.SpecEvaluator.evaluate_dict")

        @pytest.fixture
        def mock_evaluate_list(self, mocker):
            return mocker.patch("scanapi.spec_evaluator.SpecEvaluator.evaluate_list")

        @pytest.fixture
        def mock_evaluate_string(self, mocker):
            return mocker.patch("scanapi.spec_evaluator.SpecEvaluator.evaluate_string")

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
                    "scanapi.spec_evaluator.SpecEvaluator.evaluate"
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
                    "scanapi.spec_evaluator.SpecEvaluator.evaluate"
                )
                mock_evaluate.return_value = "evaluated_value"
                evaluated_list = spec_evaluator.evaluate_list(
                    ["${API_TOKEN}", "${APP_ID}"]
                )
                assert evaluated_list == ["evaluated_value", "evaluated_value"]

    class TestEvaluateString:
        # TODO
        pass

    class TestEvaluateEnvVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no env var", "${var}", "${{var}}", "${{VAR}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, spec_evaluator, sequence):
                assert spec_evaluator.evaluate_env_var(sequence) == sequence

        class TestWhenMatchesThePattern:
            class TestWhenEnvVarIsSetProperly:
                @pytest.fixture(autouse=True)
                def base_url_env(self):
                    os.environ["BASE_URL"] = "https://jsonplaceholder.typicode.com"
                    os.environ["POST_ID"] = "2"

                test_data = [
                    ("${BASE_URL}", "https://jsonplaceholder.typicode.com"),
                    ("${BASE_URL}/posts", "https://jsonplaceholder.typicode.com/posts"),
                    (
                        "https://jsonplaceholder.typicode.com/posts/${POST_ID}",
                        "https://jsonplaceholder.typicode.com/posts/2",
                    ),
                    (
                        "${BASE_URL}/posts/${POST_ID}",
                        "https://jsonplaceholder.typicode.com/posts/2",
                    ),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_evaluated_var(
                    self, spec_evaluator, sequence, expected
                ):
                    assert spec_evaluator.evaluate_env_var(sequence) == expected

            class TestWhenThereIsNoCorrespondingEnvVar:
                @pytest.fixture(autouse=True)
                def remove_base_url_env(self):
                    if os.environ.get("BASE_URL"):
                        del os.environ["BASE_URL"]

                def test_should_raise_bad_configuration_error(self, spec_evaluator):
                    with pytest.raises(BadConfigurationError) as excinfo:
                        spec_evaluator.evaluate_env_var("${BASE_URL}")

                    assert (
                        str(excinfo.value)
                        == "'BASE_URL' environment variable not set or badly configured"
                    )

    class TestEvaluateCustomVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no var", "${ENV_VAR}", "${{code}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, spec_evaluator, sequence):
                assert spec_evaluator.evaluate_custom_var(sequence) == sequence

        class TestWhenMatchesThePattern:
            class TestWhenCodeDoesNotContainThePreSavedCustomVar:
                @pytest.fixture
                def spec_evaluator(self):
                    class APITreeMock:
                        def __init__(self):
                            self.responses = {}
                            self.custom_vars = {}

                    return SpecEvaluator(APITreeMock())

                test_data = [
                    ("${user_id}"),
                    ("something before ${user_id} something after"),
                    ("something before ${user_id}"),
                    ("${user_id} something after"),
                ]

                @pytest.mark.parametrize("sequence", test_data)
                def test_should_return_response(self, spec_evaluator, mocker, sequence):
                    assert spec_evaluator.evaluate_custom_var(sequence) == sequence

            class TestWhenCodeContainsThePreSavedCustomVar:
                @pytest.fixture
                def spec_evaluator(self):
                    class APITreeMock:
                        def __init__(self):
                            self.responses = {}
                            self.custom_vars = {"user_id": "10"}

                    return SpecEvaluator(APITreeMock())

                test_data = [
                    ("${user_id}", "10"),
                    ("something before ${user_id}", "something before 10"),
                    (
                        "something before ${user_id} something after",
                        "something before 10 something after",
                    ),
                    ("${user_id} something after", "10 something after"),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_response(
                    self, spec_evaluator, mocker, sequence, expected
                ):
                    assert spec_evaluator.evaluate_custom_var(sequence) == expected

    class TestEvaluatePythonCode:
        @pytest.fixture
        def spec_evaluator(self):
            class APITreeMock:
                def __init__(self):
                    self.responses = {}

            return SpecEvaluator(APITreeMock())

        class TestWhenDoesNotMatchThePattern:
            test_data = ["no code", "${CODE}", "${code}", "{{code}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, spec_evaluator, sequence):
                assert spec_evaluator.evaluate_python_code(sequence) == sequence

        class TestWhenMatchesThePattern:
            test_data = [("${{1 + 1}}", "2"), ("${{'hi'*4}}", "hihihihi")]

            @pytest.mark.parametrize("sequence, expected", test_data)
            def test_should_return_evaluated_code(
                self, spec_evaluator, sequence, expected
            ):
                assert spec_evaluator.evaluate_python_code(sequence) == expected

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
                    self, spec_evaluator, mocker, sequence, expected
                ):
                    assert spec_evaluator.evaluate_python_code(sequence) == expected

            class TestWhenCodeBreaks:
                def test_should_raises_invalid_python_code_error(self, spec_evaluator):
                    with pytest.raises(InvalidPythonCodeError) as excinfo:
                        spec_evaluator.evaluate_python_code("${{1/0}}")

                    assert (
                        str(excinfo.value)
                        == "Invalid Python code defined in the API spec: division by zero"
                    )

    class TestReplaceVarWithValue:
        test_data = [
            ("${age}", "${age}", "45", "45"),
            ("I am ${age} years old", "${age}", "60", "I am 60 years old"),
            (
                "url/${{some['python_code']!}}",
                "${{some['python_code']!}}",
                "300",
                "url/300",
            ),
            (
                "${BASE_URL}/posts",
                "${BASE_URL}",
                "https://jsonplaceholder.typicode.com",
                "https://jsonplaceholder.typicode.com/posts",
            ),
        ]

        @pytest.mark.parametrize(
            "sequence, variable, variable_value, expected", test_data
        )
        def test_should_replace(
            self, spec_evaluator, sequence, variable, variable_value, expected
        ):
            assert (
                spec_evaluator.replace_var_with_value(
                    sequence, variable, variable_value
                )
                == expected
            )

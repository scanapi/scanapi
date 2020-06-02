import os
import pytest

from scanapi.errors import BadConfigurationError
from scanapi.evaluators import StringEvaluator


class TestStringEvaluator:
    class TestEvaluate:
        @pytest.fixture
        def mock__evaluate_env_var(self, mocker):
            mock_func = mocker.patch(
                "scanapi.evaluators.string_evaluator.StringEvaluator._evaluate_env_var"
            )
            mock_func.return_value = ""
            return mock_func

        @pytest.fixture
        def mock_code_evaluate(self, mocker):
            mock_func = mocker.patch(
                "scanapi.evaluators.code_evaluator.CodeEvaluator.evaluate"
            )
            mock_func.return_value = ""
            return mock_func

        def test_calls_code_evaluate(self, mock_code_evaluate):
            StringEvaluator.evaluate("boo", {})
            mock_code_evaluate.assert_called_once_with("boo", {}, False)

        def test_calls__evaluate_env_var(self, mock__evaluate_env_var):
            StringEvaluator.evaluate("boo", {})
            mock__evaluate_env_var.assert_called_once_with("boo")

    class TestEvaluateEnvVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no env var", "${var}", "${MyVar}", "${{var}}", "${{VAR}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert StringEvaluator._evaluate_env_var(sequence) == sequence

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
                def test_should_return_evaluated_var(self, sequence, expected):
                    assert StringEvaluator._evaluate_env_var(sequence) == expected

            class TestWhenThereIsNoCorrespondingEnvVar:
                @pytest.fixture(autouse=True)
                def remove_base_url_env(self):
                    if os.environ.get("BASE_URL"):
                        del os.environ["BASE_URL"]

                def test_should_raise_bad_configuration_error(self):
                    with pytest.raises(BadConfigurationError) as excinfo:
                        StringEvaluator._evaluate_env_var("${BASE_URL}")

                    assert (
                        str(excinfo.value)
                        == "'BASE_URL' environment variable not set or badly configured"
                    )

    class TestEvaluateCustomVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no var", "${ENV_VAR}", "${{code}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert StringEvaluator._evaluate_custom_var(sequence, {}) == sequence

        class TestWhenMatchesThePattern:
            class TestWhenCodeDoesNotContainThePreSavedCustomVar:
                test_data = [
                    ("${user_id}"),
                    ("something before ${user_id} something after"),
                    ("something before ${user_id}"),
                    ("${user_id} something after"),
                ]

                @pytest.mark.parametrize("sequence", test_data)
                def test_should_return_sequence(self, sequence):
                    assert (
                        StringEvaluator._evaluate_custom_var(sequence, {}) == sequence
                    )

            class TestWhenCodeContainsThePreSavedCustomVar:
                test_data = [
                    ("${user_id}", "10"),
                    ("${apiKey}", "abc123"),
                    ("something before ${user_id}", "something before 10"),
                    (
                        "something before ${user_id} something after",
                        "something before 10 something after",
                    ),
                    ("${user_id} something after", "10 something after"),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_sequence(self, sequence, expected):
                    vars = {"user_id": "10", "apiKey": "abc123"}
                    assert (
                        StringEvaluator._evaluate_custom_var(sequence, vars) == expected
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
        def test_should_replace(self, sequence, variable, variable_value, expected):
            assert (
                StringEvaluator.replace_var_with_value(
                    sequence, variable, variable_value
                )
                == expected
            )

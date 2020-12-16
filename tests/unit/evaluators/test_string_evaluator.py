import os

import pytest

from scanapi.errors import BadConfigurationError
from scanapi.evaluators import StringEvaluator


@pytest.mark.describe("Test String Evaluator")
class TestStringEvaluator:
    @pytest.mark.describe("Test Evaluate")
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

        @pytest.mark.it("should call code evaluate")
        def test_calls_code_evaluate(self, mock_code_evaluate):
            StringEvaluator.evaluate("boo", {})
            mock_code_evaluate.assert_called_once_with("boo", {}, False)

        @pytest.mark.it("should calls _evaluate_env_var")
        def test_calls__evaluate_env_var(self, mock__evaluate_env_var):
            StringEvaluator.evaluate("boo", {})
            mock__evaluate_env_var.assert_called_once_with("boo")

    @pytest.mark.describe("Test Evaluate Env Var")
    class TestEvaluateEnvVar:
        @pytest.mark.context("When Does Not Match The Pattern")
        class TestWhenDoesNotMatchThePattern:
            test_data = [
                "no env var",
                "${var}",
                "${MyVar}",
                "${{var}}",
                "${{VAR}}",
            ]

            @pytest.mark.context("should return sequence")
            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert StringEvaluator._evaluate_env_var(sequence) == sequence

        @pytest.mark.context("When Matches The Pattern")
        class TestWhenMatchesThePattern:
            @pytest.mark.context("When Env Var Is Set Properly")
            class TestWhenEnvVarIsSetProperly:
                @pytest.fixture(autouse=True)
                def base_url_env(self):
                    os.environ[
                        "BASE_URL"
                    ] = "https://jsonplaceholder.typicode.com"
                    os.environ["POST_ID"] = "2"

                test_data = [
                    ("${BASE_URL}", "https://jsonplaceholder.typicode.com"),
                    (
                        "${BASE_URL}/posts",
                        "https://jsonplaceholder.typicode.com/posts",
                    ),
                    (
                        "https://jsonplaceholder.typicode.com/posts/${POST_ID}",
                        "https://jsonplaceholder.typicode.com/posts/2",
                    ),
                    (
                        "${BASE_URL}/posts/${POST_ID}",
                        "https://jsonplaceholder.typicode.com/posts/2",
                    ),
                ]

                @pytest.mark.it("should return evaluated var")
                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_evaluated_var(self, sequence, expected):
                    assert (
                        StringEvaluator._evaluate_env_var(sequence) == expected
                    )

            @pytest.mark.context("When There Is No Corresponding Env Var")
            class TestWhenThereIsNoCorrespondingEnvVar:
                @pytest.fixture(autouse=True)
                def remove_base_url_env(self):
                    if os.environ.get("BASE_URL"):
                        del os.environ["BASE_URL"]

                @pytest.mark.it("should raise bad configuration error")
                def test_should_raise_bad_configuration_error(self):
                    with pytest.raises(BadConfigurationError) as excinfo:
                        StringEvaluator._evaluate_env_var("${BASE_URL}")

                    assert (
                        str(excinfo.value)
                        == "'BASE_URL' environment variable not set or badly configured"
                    )

    @pytest.mark.describe("Test Evaluate Custom Var")
    class TestEvaluateCustomVar:
        @pytest.mark.context("When Does Not Match The Pattern")
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no var", "${ENV_VAR}", "${{code}}"]

            @pytest.mark.it("should return sequence")
            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert (
                    StringEvaluator._evaluate_custom_var(sequence, {})
                    == sequence
                )

        @pytest.mark.context("When Matches The Pattern")
        class TestWhenMatchesThePattern:
            @pytest.mark.context(
                "When Code Does Not Contain The Pre Saved CustomVar"
            )
            class TestWhenCodeDoesNotContainThePreSavedCustomVar:
                test_data = [
                    ("${user_id}"),
                    ("${user-id}"),
                    ("something before ${user_id} something after"),
                    ("something before ${user_id}"),
                    ("${user_id} something after"),
                ]

                @pytest.mark.it("should return sequence")
                @pytest.mark.parametrize("sequence", test_data)
                def test_should_return_sequence(self, sequence):
                    assert (
                        StringEvaluator._evaluate_custom_var(sequence, {})
                        == sequence
                    )

            @pytest.mark.context("When Code Contains The Pre Saved CustomVar")
            class TestWhenCodeContainsThePreSavedCustomVar:
                test_data = [
                    ("${user_id}", "10"),
                    ("${apiKey}", "abc123"),
                    ("${api-token}", "xwo"),
                    ("something before ${user_id}", "something before 10"),
                    (
                        "something before ${user_id} something after",
                        "something before 10 something after",
                    ),
                    ("${user_id} something after", "10 something after"),
                ]

                @pytest.mark.it("should return sequence")
                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_sequence(self, sequence, expected):
                    vars = {
                        "user_id": "10",
                        "apiKey": "abc123",
                        "api-token": "xwo",
                    }
                    assert (
                        StringEvaluator._evaluate_custom_var(sequence, vars)
                        == expected
                    )

    @pytest.mark.describe("Test Replace Var With Value")
    class TestReplaceVarWithValue:
        test_data = [
            ("${age}", "${age}", "45", "45"),
            ("${USER-AGE}", "${USER-AGE}", "45", "45"),
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
            ("${product_id}", "${product_id}", 100, 100),
            ("products/${product_id}", "${product_id}", 100, "products/100"),
        ]

        @pytest.mark.describe("should replace")
        @pytest.mark.parametrize(
            "sequence, variable, variable_value, expected", test_data
        )
        def test_should_replace(
            self, sequence, variable, variable_value, expected
        ):
            assert (
                StringEvaluator.replace_var_with_value(
                    sequence, variable, variable_value
                )
                == expected
            )

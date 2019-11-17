import os
import pytest

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.evaluators.spec_evaluator import SpecEvaluator
from scanapi.evaluators.string_evaluator import StringEvaluator


class TestStringEvaluator:
    @pytest.fixture
    def spec_evaluator(self):
        return SpecEvaluator({})

    @pytest.fixture
    def string_evaluator(self, spec_evaluator):
        return StringEvaluator(spec_evaluator)

    class TestEvaluate:
        # TODO
        pass

    class TestEvaluateEnvVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no env var", "${var}", "${{var}}", "${{VAR}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, string_evaluator, sequence):
                assert string_evaluator.evaluate_env_var(sequence) == sequence

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
                    self, string_evaluator, sequence, expected
                ):
                    assert string_evaluator.evaluate_env_var(sequence) == expected

            class TestWhenThereIsNoCorrespondingEnvVar:
                @pytest.fixture(autouse=True)
                def remove_base_url_env(self):
                    if os.environ.get("BASE_URL"):
                        del os.environ["BASE_URL"]

                def test_should_raise_bad_configuration_error(self, string_evaluator):
                    with pytest.raises(BadConfigurationError) as excinfo:
                        string_evaluator.evaluate_env_var("${BASE_URL}")

                    assert (
                        str(excinfo.value)
                        == "'BASE_URL' environment variable not set or badly configured"
                    )

    class TestEvaluateCustomVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no var", "${ENV_VAR}", "${{code}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, string_evaluator, sequence):
                assert string_evaluator.evaluate_custom_var(sequence) == sequence

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
                def test_should_return_response(
                    self, string_evaluator, mocker, sequence
                ):
                    assert string_evaluator.evaluate_custom_var(sequence) == sequence

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
                    self, string_evaluator, mocker, sequence, expected
                ):
                    assert string_evaluator.evaluate_custom_var(sequence) == expected

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
            self, string_evaluator, sequence, variable, variable_value, expected
        ):
            assert (
                string_evaluator.replace_var_with_value(
                    sequence, variable, variable_value
                )
                == expected
            )

import os

from pytest import fixture, mark, raises

from scanapi.errors import BadConfigurationError
from scanapi.evaluators import StringEvaluator


@mark.describe("string evaluator")
@mark.describe("evaluate")
class TestEvaluate:
    @fixture
    def mock__evaluate_env_var(self, mocker):
        mock_func = mocker.patch(
            "scanapi.evaluators.string_evaluator.StringEvaluator._evaluate_env_var"
        )
        mock_func.return_value = ""
        return mock_func

    @fixture
    def mock_code_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.evaluators.code_evaluator.CodeEvaluator.evaluate"
        )
        mock_func.return_value = ""
        return mock_func

    @mark.it("should call code evaluate")
    def test_calls_code_evaluate(self, mock_code_evaluate):
        StringEvaluator.evaluate("boo", {})
        mock_code_evaluate.assert_called_once_with("boo", {}, False)

    @mark.it("should calls _evaluate_env_var")
    def test_calls__evaluate_env_var(self, mock__evaluate_env_var):
        StringEvaluator.evaluate("boo", {})
        mock__evaluate_env_var.assert_called_once_with("boo")


@mark.describe("string evaluator")
@mark.describe("_evaluate_env_var")
class TestEvaluateEnvVar:
    test_data = [
        "no env var",
        "${var}",
        "${MyVar}",
        "${{var}}",
        "${{VAR}}",
    ]

    @mark.context("when does not match the pattern")
    @mark.it("should return sequence")
    @mark.parametrize("sequence", test_data)
    def test_should_return_sequence(self, sequence):
        assert StringEvaluator._evaluate_env_var(sequence) == sequence

    test_data = [
        ("${BASE_URL}", "https://jsonplaceholder.typicode.com"),
        ("${BASE_URL}/posts", "https://jsonplaceholder.typicode.com/posts",),
        (
            "https://jsonplaceholder.typicode.com/posts/${POST_ID}",
            "https://jsonplaceholder.typicode.com/posts/2",
        ),
        (
            "${BASE_URL}/posts/${POST_ID}",
            "https://jsonplaceholder.typicode.com/posts/2",
        ),
    ]

    @mark.context("when matches the pattern")
    @mark.context("when env var is set properly")
    @mark.it("should return sequence with evaluated var")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_evaluated_var(self, sequence, expected):
        os.environ["BASE_URL"] = "https://jsonplaceholder.typicode.com"
        os.environ["POST_ID"] = "2"

        assert StringEvaluator._evaluate_env_var(sequence) == expected

    @mark.context("when matches the pattern")
    @mark.context("when there is no corresponding env var")
    @mark.it("should raise bad configuration error")
    def test_should_raise_bad_configuration_error(self):
        if os.environ.get("BASE_URL"):
            del os.environ["BASE_URL"]

        with raises(BadConfigurationError) as excinfo:
            StringEvaluator._evaluate_env_var("${BASE_URL}")

            assert (
                str(excinfo.value)
                == "'BASE_URL' environment variable not set or badly configured"
            )


@mark.describe("string evaluator")
@mark.describe("_evaluate_custom_var")
class TestEvaluateCustomVar:
    test_data = ["no var", "${ENV_VAR}", "${{code}}"]

    @mark.context("when does not match the pattern")
    @mark.it("should return sequence")
    @mark.parametrize("sequence", test_data)
    def test_should_return_sequence(self, sequence):
        assert StringEvaluator._evaluate_custom_var(sequence, {}) == sequence

    test_data = [
        ("${user_id}"),
        ("${user-id}"),
        ("something before ${user_id} something after"),
        ("something before ${user_id}"),
        ("${user_id} something after"),
    ]

    @mark.context("when matches the pattern")
    @mark.context("when code does not contain the pre saved customvar")
    @mark.it("should return sequence")
    @mark.parametrize("sequence", test_data)
    def test_should_return_sequence_2(self, sequence):
        assert StringEvaluator._evaluate_custom_var(sequence, {}) == sequence

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

    @mark.context("when matches the pattern")
    @mark.context("when code contains the pre saved customvar")
    @mark.it("should return sequence with evaluated custom var")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_sequence_3(self, sequence, expected):
        spec_vars = {
            "user_id": "10",
            "apiKey": "abc123",
            "api-token": "xwo",
        }
        assert (
            StringEvaluator._evaluate_custom_var(sequence, spec_vars)
            == expected
        )


@mark.describe("string evaluator")
@mark.describe("replace_var_with_value")
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

    @mark.describe("replace var with value")
    @mark.it("should replace")
    @mark.parametrize("sequence, variable, variable_value, expected", test_data)
    def test_should_replace(self, sequence, variable, variable_value, expected):
        assert (
            StringEvaluator.replace_var_with_value(
                sequence, variable, variable_value
            )
            == expected
        )

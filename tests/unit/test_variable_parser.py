import os
import pytest

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.variable_parser import (
    evaluate_env_var,
    evaluate_python_code,
    evaluate_var,
    responses,
    save_response,
)


class TestVariableParser:
    class TestEvaluate:
        # TODO
        pass

    class TestEvaluateDict:
        # TODO
        pass

    class TestEvaluateEnvVar:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no env var", "${var}", "${{var}}", "${{VAR}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert evaluate_env_var(sequence) == sequence

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
                    assert evaluate_env_var(sequence) == expected

            class TestWhenThereIsNoCorrespondingEnvVar:
                @pytest.fixture(autouse=True)
                def remove_base_url_env(self):
                    if os.environ.get("BASE_URL"):
                        del os.environ["BASE_URL"]

                def test_should_raise_bad_configuration_error(self):
                    with pytest.raises(BadConfigurationError) as excinfo:
                        evaluate_env_var("${BASE_URL}")

                    assert (
                        str(excinfo.value)
                        == "'BASE_URL' environment variable not set or badly configured"
                    )

    class TestEvaluateCustomVar:
        # TODO
        pass

    class TestEvaluateVar:
        test_data = [
            ("${age}", "${age}", "45", "45"),
            ("I am ${age} years old", "${age}", "60", "I am 60 years old"),
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
        def test_should_replace_var(self, sequence, variable, variable_value, expected):
            assert evaluate_var(sequence, variable, variable_value) == expected

    class TestEvaluatePythonCode:
        class TestWhenDoesNotMatchThePattern:
            test_data = [
                "no code",
                "${CODE}",
                "${code}",
                "something before ${{code}} something after",
                "${{code}} something after",
                "something before ${{code}}",
                " ${{code}} ",
            ]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert evaluate_python_code(sequence) == sequence

        class TestWhenMatchesThePattern:
            test_data = [("${{1 + 1}}", "2"), ("${{'hi'*4}}", "hihihihi")]

            @pytest.mark.parametrize("sequence, expected", test_data)
            def test_should_return_evaluated_code(self, sequence, expected):
                assert evaluate_python_code(sequence) == expected

            class TestWhenCodeContainsPreSavedRequest:
                test_data = [
                    ("${{responses['user_details'].json()[0]['id']}}", "1"),
                    ("${{responses['user_details'].json()[0]['name']}}", "John"),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_response(self, mocker, sequence, expected):
                    response = mocker.MagicMock()
                    response.json.return_value = [{"id": 1, "name": "John"}]
                    save_response("user_details", response)

                    assert evaluate_python_code(sequence) == expected

            class TestWhenCodeBreaks:
                def test_should_raises_invalid_python_code_error(self):
                    with pytest.raises(InvalidPythonCodeError) as excinfo:
                        evaluate_python_code("${{1/0}}")

                    assert (
                        str(excinfo.value)
                        == "Invalid Python code defined in the API spec: division by zero"
                    )

    class TestSaveResponse:
        def test_should_retrieve_the_saved_response(self, mocker):
            response = mocker.MagicMock()
            save_response("fake_request", response)

            assert responses["fake_request"] == response

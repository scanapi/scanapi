import requests
from pytest import fixture, mark, raises

from scanapi.errors import InvalidPythonCodeError
from scanapi.evaluators import CodeEvaluator


@mark.describe("code evaluator")
@mark.describe("evaluate")
class TestEvaluate:
    @fixture
    def response(self, requests_mock):
        requests_mock.get("http://test.com", text="abcde")
        return requests.get("http://test.com")

    test_data = ["no code", "${CODE}", "${code}", "{{code}}", 10, []]

    @mark.context("when sequence does not match the pattern")
    @mark.it("should return sequence")
    @mark.parametrize("sequence", test_data)
    def test_should_return_sequence(self, sequence):
        assert CodeEvaluator.evaluate(sequence, {}) == sequence

    test_data = [
        ("${{1 == 1}}", (True, None)),
        ("${{1 == 4}}", (False, "1 == 4")),
    ]

    @mark.context("when sequence matches the pattern")
    @mark.context("when it is a test case")
    @mark.context("when code does not contain pre saved response")
    @mark.it("should return assert results")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_assert_results(self, sequence, expected):
        assert (
            CodeEvaluator.evaluate(sequence, {}, is_a_test_case=True)
            == expected
        )

    test_data = [
        ("${{response.text == 'abcde'}}", (True, None)),
        ("${{response.url == 'http://test.com/'}}", (True, None),),
        (
            "${{response.status_code == 300}}",
            (False, "response.status_code == 300"),
        ),
        ("${{response.url == 'abc'}}", (False, "response.url == 'abc'"),),
    ]

    @mark.context("when sequence matches the pattern")
    @mark.context("when it is a test case")
    @mark.context("when code contains pre saved response")
    @mark.it("should return assert results")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_assert_results_2(self, sequence, expected, response):
        assert (
            CodeEvaluator.evaluate(
                sequence, {"response": response}, is_a_test_case=True,
            )
            == expected
        )

    test_data = [
        ("${{1/0}}", {}, True),
        ("${{response.url == 'abc'}}", {}, True),
        ("${{foo = 'abc'}}", {}, True),
    ]

    @mark.context("when sequence matches the pattern")
    @mark.context("when it is a test case")
    @mark.context("when code breaks")
    @mark.it("should raises invalid python code error")
    @mark.parametrize("sequence, spec_vars, is_a_test_case", test_data)
    def test_should_raises_invalid_python_code_error(
        self, sequence, spec_vars, is_a_test_case
    ):
        with raises(InvalidPythonCodeError) as excinfo:
            CodeEvaluator.evaluate(sequence, spec_vars, is_a_test_case)

        assert isinstance(excinfo.value, InvalidPythonCodeError)

    test_data = [("${{1 + 1}}", "2"), ("${{'hi'*4}}", "hihihihi")]

    @mark.context("when sequence matches the pattern")
    @mark.context("when it is not a test case")
    @mark.context("when code does not contain pre saved response")
    @mark.it("should return evaluated code")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_evaluated_code(self, sequence, expected):
        assert CodeEvaluator.evaluate(sequence, {}) == expected

    test_data = [
        ("${{response.text}}", "abcde"),
        ("${{response.status_code}}", "200"),
        ("${{response.text + 'xpto'}}", "abcdexpto"),
        ("${{'xpto' + response.text}}", "xptoabcde"),
        ("${{1+1}}", "2"),
    ]

    @mark.context("when sequence matches the pattern")
    @mark.context("when it is not a test case")
    @mark.context("when code contains pre saved response")
    @mark.it("should return evaluated code")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_evaluated_code_2(self, sequence, expected, response):
        assert (
            CodeEvaluator.evaluate(sequence, {"response": response}) == expected
        )

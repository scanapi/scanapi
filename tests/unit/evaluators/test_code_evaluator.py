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
        (
            "${{response.url == 'http://test.com/'}}",
            (True, None),
        ),
        ("${{all(x in response.text for x in 'abc')}}", (True, None)),
        (
            "${{response.status_code == 300}}",
            (False, "response.status_code == 300"),
        ),
        (
            "${{response.url == 'abc'}}",
            (False, "response.url == 'abc'"),
        ),
    ]

    @mark.context("when sequence matches the pattern")
    @mark.context("when it is a test case")
    @mark.context("when code contains pre saved response")
    @mark.it("should return assert results")
    @mark.parametrize("sequence, expected", test_data)
    def test_should_return_assert_results_2(self, sequence, expected, response):
        assert (
            CodeEvaluator.evaluate(
                sequence,
                {"response": response},
                is_a_test_case=True,
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


@mark.describe("TestAllowedModules")
class TestAllowedModules:
    """Test that only modules in ALLOWED_MODULES are accessible"""

    test_data = [
        ("${{datetime.datetime.now().year >= 2020}}", True),
        ("${{math.sqrt(16)}}", "4.0"),
        ("${{math.pi > 3}}", True),
        ("${{random.randint(1, 1)}}", "1"),
        ("${{re.match('a', 'abc') is not None}}", True),
        ("${{time.time() > 0}}", True),
        ("${{str(uuid.uuid4())}}", str),  # Check it's a string
    ]

    @mark.context("when using allowed modules")
    @mark.it("should allow access to ALLOWED_MODULES")
    @mark.parametrize("sequence, expected_type", test_data)
    def test_allowed_modules_work(self, sequence, expected_type):
        result = CodeEvaluator.evaluate(sequence, {})
        if expected_type == str:
            assert isinstance(result, str)
            assert len(result) > 0
        elif isinstance(expected_type, bool):
            assert (
                CodeEvaluator.evaluate(sequence, {}, is_a_test_case=True)[0]
                == expected_type
            )
        else:
            assert result == expected_type


@mark.describe("TestDisallowedModules")
class TestDisallowedModules:
    """Test that modules not in ALLOWED_MODULES are blocked"""

    test_data = [
        "${{__import__('os').system('ls')}}",
        "${{__import__('subprocess').call(['echo', 'hello'])}}",
        "${{__import__('sys').exit(1)}}",
        "${{__import__('socket').create_connection(('127.0.0.1', 80))}}",
        "${{__import__('urllib.request').urlopen('http://example.com')}}",
        "${{__import__('builtins').open('/etc/passwd')}}",
    ]

    @mark.context("when trying to import disallowed modules")
    @mark.it("should raise InvalidPythonCodeError")
    @mark.parametrize("sequence", test_data)
    def test_disallowed_modules_blocked(self, sequence):
        with raises(InvalidPythonCodeError):
            CodeEvaluator.evaluate(sequence, {})


@mark.describe("TestSafeBuiltins")
class TestSafeBuiltins:
    """Test that dangerous built-ins are blocked"""

    test_data = [
        "${{open('/etc/passwd')}}",
        "${{exec('print(1)')}}",
        "${{eval('2+2')}}",
        "${{compile('1+1', '<string>', 'eval')}}",
        "${{__import__('os')}}",
        "${{globals()}}",
        "${{locals()}}",
        "${{vars()}}",
        "${{dir()}}",
    ]

    @mark.context("when trying to use dangerous built-ins")
    @mark.it("should raise InvalidPythonCodeError")
    @mark.parametrize("sequence", test_data)
    def test_dangerous_builtins_blocked(self, sequence):
        with raises(InvalidPythonCodeError):
            CodeEvaluator.evaluate(sequence, {})

    allowed_builtins_data = [
        ("${{len('hello')}}", "5"),
        ("${{str(42)}}", "42"),
        ("${{all([True, True])}}", True),
        ("${{any([False, True])}}", True),
    ]

    @mark.context("when using safe built-ins")
    @mark.it("should work correctly")
    @mark.parametrize("sequence, expected", allowed_builtins_data)
    def test_safe_builtins_work(self, sequence, expected):
        if isinstance(expected, bool):
            assert (
                CodeEvaluator.evaluate(sequence, {}, is_a_test_case=True)[0]
                == expected
            )
        else:
            assert CodeEvaluator.evaluate(sequence, {}) == expected


@mark.describe("TestRestrictedAttributes")
class TestRestrictedAttributes:
    """Test that dunder attributes and dangerous methods are blocked"""

    test_data = [
        "${{().__class__.__mro__}}",
        "${{(lambda:0).__globals__}}",
        "${{().__class__.__bases__}}",
        "${{''.__class__.__mro__[1].__subclasses__()}}",
        "${{().__class__.__bases__[0].__subclasses__()}}",
    ]

    @mark.context("when trying to access restricted attributes")
    @mark.it("should raise InvalidPythonCodeError")
    @mark.parametrize("sequence", test_data)
    def test_restricted_attributes_blocked(self, sequence):
        with raises(InvalidPythonCodeError):
            CodeEvaluator.evaluate(sequence, {})


@mark.describe("TestSideEffects")
class TestSideEffects:
    """Test that evaluations don't have persistent side effects"""

    @mark.context("when evaluating expressions")
    @mark.it("should not persist variables between evaluations")
    def test_no_variable_persistence(self):
        # This should not affect subsequent evaluations
        with raises(InvalidPythonCodeError):
            CodeEvaluator.evaluate("${{x = 42}}", {})

        # This should still fail because x shouldn't persist
        with raises(InvalidPythonCodeError):
            CodeEvaluator.evaluate("${{x}}", {})

    @mark.context("when evaluating multiple expressions")
    @mark.it("should be isolated from each other")
    def test_evaluation_isolation(self):
        result1 = CodeEvaluator.evaluate("${{len('a')}}", {})
        result2 = CodeEvaluator.evaluate("${{len('bb')}}", {})

        assert result1 == "1"
        assert result2 == "2"


@mark.describe("TestErrorMessages")
class TestErrorMessages:
    """Test that error messages include both helpful message and offending code"""

    test_data = [
        ("${{1/0}}", "1/0"),
        ("${{undefined_var}}", "undefined_var"),
        ("${{invalid syntax here}}", "invalid syntax here"),
        ("${{open('/nonexistent')}}", "open('/nonexistent')"),
    ]

    @mark.context("when code evaluation fails")
    @mark.it("should include offending code in error message")
    @mark.parametrize("sequence, expected_code", test_data)
    def test_error_includes_offending_code(self, sequence, expected_code):
        with raises(InvalidPythonCodeError) as excinfo:
            CodeEvaluator.evaluate(sequence, {})

        error = excinfo.value
        assert hasattr(
            error, "expression"
        ), "Error should have expression attribute"
        assert expected_code in error.expression


@mark.describe("TestUnicodeHandling")
class TestUnicodeHandling:
    """Test correct behavior with Unicode and non-ASCII content"""

    test_data = [
        ("${{u'áéíóú'[::-1]}}", "úóíéá"),
        ("${{len('café')}}", "4"),
        ("${{u'héllo'.upper()}}", "HÉLLO"),
        ("${{'ñoño' + 'mañana'}}", "ñoñomañana"),
        ("${{u'中文测试'.encode('utf-8').decode('utf-8')}}", "中文测试"),
    ]

    @mark.context("when using Unicode strings")
    @mark.it("should handle non-ASCII content correctly")
    @mark.parametrize("sequence, expected", test_data)
    def test_unicode_handling(self, sequence, expected):
        result = CodeEvaluator.evaluate(sequence, {})
        assert result == expected

    @mark.context("when using Unicode variable names")
    @mark.it("should prevent Unicode identifier injection")
    def test_unicode_identifiers_restricted(self):
        # This should fail - we don't allow assignment
        with raises(InvalidPythonCodeError):
            CodeEvaluator.evaluate("${{á = 42}}", {})

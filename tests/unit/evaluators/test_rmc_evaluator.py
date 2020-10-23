import ast
from unittest.mock import Mock

import pytest
import scanapi
from scanapi.evaluators import rmc_evaluator as rmc


rmc_eval = rmc.RemoteMethodCallEvaluator.evaluate


class TestRemoteMethodCallEvaluator:
    class TestGetName:
        def test_expected_behavior(self):
            assert rmc.getname("evaluators.rmc_evaluator", scanapi) == rmc
            import functools

            assert (
                rmc.getname("partial.__module__", functools)
                == functools.partial.__module__
            )

        class TestWhenNameDoesntExist:
            def test_should_raise_attribute_error(self):
                with pytest.raises(AttributeError) as excinfo:
                    rmc.getname("evaluators.rmc_evaltor", scanapi) == rmc
                assert str(excinfo.value) == (
                    f"No such location: {scanapi}.evaluators.rmc_evaltor"
                )

    class TestUnrollName:
        def test_expected_behavior(self):
            assert rmc.unroll_name(ast.parse("a", mode="eval").body) == "a"
            assert rmc.unroll_name(ast.parse("a.c", mode="eval").body) == "a.c"
            assert rmc.unroll_name(ast.parse("a.b.c", mode="eval").body) == "a.b.c"

    class TestEvaluate:
        class TestWhenCodeRightMemberIsInvalid:
            def test_expected_behavior(self):
                with pytest.raises(ValueError) as excinfo:
                    rmc_eval("a:b + c", {})
                assert str(excinfo.value) == (
                    "Failed to parse 'b + c' as an attribute name or function call."
                )

        class TestOnlyBareName:
            def test_expected_behavior(self):
                # local path module
                assert not rmc_eval(
                    "scanapi.std:response.ok", {"response": Mock(status_code=400)}
                )
                assert rmc_eval(
                    "scanapi.std:response.ok", {"response": Mock(status_code=200)}
                )

                # no spec
                assert rmc_eval("builtins:str", {"object": {4}}) == "{'object': {4}}"

                # spec but doesn't take keyword arguments
                assert rmc_eval("builtins:list", {"iterable": (4, 5)}) == ["iterable"]

        class TestExprWithPositionalArgs:
            def test_expected_behavior(self):
                assert rmc_eval(
                    "scanapi.std:response.status_is(200)",
                    {"response": Mock(status_code=200)},
                )
                assert not rmc_eval(
                    "scanapi.std:response.status_is(200)",
                    {"response": Mock(status_code=400)},
                )

        class TestExprWithKeywordArgs:
            def test_expected_behavior(self):
                assert rmc_eval(
                    "scanapi.std:response.status_is(code=200)",
                    {"response": Mock(status_code=200)},
                )
                assert not rmc_eval(
                    "scanapi.std:response.status_is(code=200)",
                    {"response": Mock(status_code=400)},
                )

        class TestExprWithStdConst:
            def test_expected_behavior(self):
                assert not rmc_eval(
                    "std:response.ok", {"response": Mock(status_code=400)}
                )
                assert not rmc_eval(":response.ok", {"response": Mock(status_code=400)})

    class TestGetModule:
        def test_expected_behavior(self):
            assert hasattr(rmc.get_module("scanapi.std"), "response")
            assert hasattr(rmc.get_module("operator"), "__add__")
            assert hasattr(rmc.get_module("pathlib"), "Path")

    class TestCallAgainstVars:
        def test_expected_behavior(self):
            def f(a: int, b: int) -> int:
                return a + b

            assert rmc.call_against_vars(f, (), {}, {"a": 3, "b": 4}) == 7
            assert rmc.call_against_vars(f, (), {"b": 4}, {"a": 3}) == 7
            assert rmc.call_against_vars(f, (3,), {}, {"b": 4}) == 7

        class TestWhenVarsIsEmpty:
            def test_should_raise_runtime_error(self):
                def f(a: int, b: int) -> int:
                    return a + b

                # vars should never be empty, so this fails
                vars = {}
                vars["vars"] = vars
                with pytest.raises(RuntimeError) as excinfo:
                    assert rmc.call_against_vars(f, (3,), {"b": 4}, vars) == 7

                assert str(excinfo.value) == (
                    f"vars={vars.keys()} contain no key that function {f} expects as parameter"
                )

        class TestWhenVarsIsNotDictLike:
            def test_should_raise_type_error(self):
                with pytest.raises(TypeError) as excinfo:
                    assert rmc.call_against_vars(lambda m: m, (), {}, 44)
                assert str(excinfo.value) == "vars=44 is not dict-like"

        class TestWhenFuncIsBuiltin:
            def test_should_use_vars_as_pos_arg(self):
                vars = {"a": 3}
                assert rmc.call_against_vars(str, (), {}, vars) == str(vars)
                assert rmc.call_against_vars(list, (), {}, vars) == list(vars)

        class TestWhenVarsIsPartOfSpec:
            def test_should_feed_vars_as_keyword_arg(self):
                def f(vars) -> int:
                    return vars["a"] + vars["b"]

                assert rmc.call_against_vars(f, (), {}, {"a": 3, "b": 4}) == 7

        class TestWhenSpecAndVarsShareNoCommonKeys:
            def test_should_raise_runtime_error(self):
                def f(args) -> int:
                    return args["a"] + args["b"]

                vars = {"a": 3, "b": 4}
                vars["vars"] = vars

                with pytest.raises(RuntimeError) as excinfo:
                    rmc.call_against_vars(f, (), {}, vars) == 7

                assert str(excinfo.value) == (
                    f"vars={vars.keys()} contain no key that function {f} expects as parameter"
                )

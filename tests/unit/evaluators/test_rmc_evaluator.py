import ast

from scanapi.evaluators.rmc_evaluator import RemoteMethodCallEvaluator, get_module, unroll_name

from unittest.mock import Mock


def test_unroll_name():

    assert unroll_name(ast.parse('a', mode='eval').body) == 'a'
    assert unroll_name(ast.parse('a.c', mode='eval').body) == 'a.c'
    assert unroll_name(ast.parse('a.b.c', mode='eval').body) == 'a.b.c'


def test_rmc():

    rmc = RemoteMethodCallEvaluator.evaluate

    # bare name
    assert rmc('scanapi.std:response.ok', {'response': Mock(status_code=400)}) == False
    assert rmc('scanapi.std:response.ok', {'response': Mock(status_code=200)}) == True

    # with args
    assert rmc('scanapi.std:response.status_is(200)', {'response': Mock(status_code=200)}) == True
    assert rmc('scanapi.std:response.status_is(200)', {'response': Mock(status_code=400)}) == False

    # with kwargs
    assert rmc('scanapi.std:response.status_is(code=200)', {'response': Mock(status_code=200)}) == True
    assert rmc('scanapi.std:response.status_is(code=200)', {'response': Mock(status_code=400)}) == False


def test_std():

    rmc = RemoteMethodCallEvaluator.evaluate

    assert rmc('std:response.ok', {'response': Mock(status_code=400)}) == False
    assert rmc(':response.ok', {'response': Mock(status_code=400)}) == False


def test_get_module():
    assert hasattr(get_module('scanapi.std'), 'response')
    assert hasattr(get_module('operator'), '__add__')
    assert hasattr(get_module('pathlib'), 'Path')

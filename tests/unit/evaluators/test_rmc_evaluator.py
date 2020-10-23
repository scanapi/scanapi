
from scanapi.evaluators.rmc import remote_method_call, get_module

from unittest.mock import Mock


def test_rmc():

    rmc = remote_method_call

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

    rmc = remote_method_call

    assert rmc('std:response.ok', {'response': Mock(status_code=400)}) == False
    assert rmc(':response.ok', {'response': Mock(status_code=400)}) == False


def test_get_module():
    assert hasattr(get_module('scanapi.std'), 'response')
    assert hasattr(get_module('operator'), '__add__')
    assert hasattr(get_module('pathlib'), 'Path')

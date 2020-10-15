from typing import Dict, Any, List, Tuple, Optional, Callable
import os
import sys
import ast
import re
import operator
from functools import partial
import importlib
import inspect
from unittest.mock import Mock


_cwd = os.getcwd()
_sentinel = object()


def rpartial(f, *a, **kw):
    if not a and not kw:
        return f
    def rpartialer(*_a, **_kw):
        __a = (*_a, *a)
        __kw = dict(kw)
        __kw.update(_kw)
        return f(*__a, **__kw)
    return rpartialer


def get_module(name: str):
    global _cwd
    if _cwd is None:
        _cwd = os.getcwd()
        sys.path.append(_cwd)
    module = sys.modules.get(name) or importlib.import_module(name)
    print(f'Loaded {module}')
    return module


def fetch(location: str) -> Callable:
    # Search for a module named after it in sys ?
    # Look at the bottom of the stack then import wildly ? or _cwd
    # Your choice
    module_name, *trail = location.split('.')
    if not trail:
        raise Exception
    module = get_module(module_name)
    node = module
    i = 0
    for i, name in enumerate(trail):
        next_node = getattr(node, name, _sentinel)
        if next_node is _sentinel:
            if type(node) is type(module):
                print('No attribute found. Trying to import as submodule ')
                try:
                    next_node = importlib.import_module(name, package=node.__name__)
                except ModuleNotFoundError:
                    pass
        if next_node is _sentinel:
            raise AttributeError(f'No such location: {module_name}.{".".join(trail[:i + 1])}')
        node = next_node
    return node


def as_kw(token: str) -> Optional[re.Match]:
    return re.match(r'^([\w.-]+)\s*=+\s*(.*)$', token)


def safe_eval(expr: str) -> Any:
    try:
        return ast.literal_eval(expr)
    except SyntaxError as e:
        e.args = (*e.args, expr)
        raise


def parse(args: str, allow_position_marker: bool = False) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    """Parse a comma-separated list of simple Python expressions."""
    right_bind = False
    tokens = re.split(r',(?!\)|\]|\})', args)
    tokens = list(map(str.strip, tokens))
    if tokens[0] == '/':
        right_bind = True
        tokens = tokens[1:]
    a = list(token for token in tokens if as_kw(token) is None)
    kw = dict(i.groups() for i in map(as_kw, tokens) if i is not None)
    for i, item in enumerate(a): a[i] = safe_eval(item)
    for name, kwarg in kw.items(): kw[name] = safe_eval(kwarg)
    if allow_position_marker:
        return tuple(a), kw, right_bind
    return tuple(a), kw


def remote_method_call(
    expr: str,
    vars: Dict[str, Any],
    is_a_test_case: bool = False
):
    expr = str(expr)
    print(f'expr = {expr}')
    print(f'vars = {vars}')

    #
    
    # Parse expr
    regex = r'^!([\w.]+)(?:\((.*)\))?$'
    m = re.match(regex, expr)
    if m is None:
        raise ValueError(f'Could not parse ! expr {expr!r}')
    name, argexpr = m.groups()
    print('name =', name)
    print('argexpr =', argexpr)

    # Build f
    f = fetch(name)
    spec = inspect.getfullargspec(f)

    if argexpr:
        a, kw, right_bind = parse(argexpr, allow_position_marker=True)
        print('a =', a)
        print('kw =', kw)
        if not right_bind:
            f = partial(f, *a, **kw)
        else:
            f = rpartial(f, *a, **kw)
    #

    args = []
    # for key in spec.args:
    #     if key not in vars:
    #         break
    #     args.append(vars[key])
    kwargs = {k: vars[k] for k in vars.keys() & {*spec.kwonlyargs, *spec.args}}
    # ^ this collide with right_bind
    result = f(*args, **kwargs)
    #or f(**vars) but need to filter suitable args from spec first

    if is_a_test_case:
        return (True, None) if operator.truth(result) else (False, expr)

    return result


def test_rmc():

    rmc = remote_method_call
    
    assert rmc('!test.it', {'a': 3}) == 3
    assert rmc('!test.it.it', {'a': 3}) == 3
    assert rmc('!test.it(b=4)', {'a': 3}) == 7

    assert rmc('!test.response.ok', {'response': Mock(status=400)}) == False

    assert rmc('!test.response.ok', {'response': Mock(status=200)}) == True

    assert rmc('!test.response.status_is(code=200)', {'response': Mock(status=200)}) == True
    assert rmc('!test.response.status_is(code=200)', {'response': Mock(status=400)}) == False

    assert rmc('!test.response.status_is(200)', {'response': Mock(status=200)}) == True
    assert rmc('!test.response.status_is(200)', {'response': Mock(status=400)}) == False


def test_get_module():
    assert hasattr(get_module('test'), 'it')
    assert hasattr(get_module('operator'), '__add__')
    assert hasattr(get_module('pathlib'), 'Path')


def test_parse():

    assert parse('3') == ((3,), {})
    assert parse('"jon"') == (('jon',), {})
    assert parse('("jon")') == (('jon',), {})
    assert parse('("jon",)') == ((('jon',),), {})

    assert parse('3, 4') == ((3, 4), {})
  
    assert parse('3, b=5') == ((3,), {'b': 5})
    assert parse('3, b=5, c=4') == ((3,), {'b': 5, 'c': 4})
    assert parse('3, b=5, 66, c.x=4') == ((3, 66), {'b': 5, 'c.x': 4})

    assert parse('3, b=5, c.x=4') == ((3,), {'b': 5, 'c.x': 4})
    assert parse('3, b==5') == ((3,), {'b': 5})

    try:
        parse('/, 3')
    except SyntaxError as e:
        assert e.args[:-1] == '/'
        
    assert parse('3', allow_position_marker=True) == ((3,), {}, False)
    assert parse('/, 3', allow_position_marker=True) == ((3,), {}, True)


def test_as_kw():
    assert as_kw('b=5') and as_kw('b=5').groups() == ('b', '5')
    assert not as_kw('3')


def test_safe_eval():

    assert safe_eval('3') == 3

    try:
        safe_eval('3+') == 3
    except SyntaxError as e:
        *_, a = e.args
        assert '3+' == a


def test_rpartial():

    def f(a, b, c, d):
        return a, b, c, d

    assert rpartial(f) == f
    assert rpartial(f, 5)(2, 3, 4) == (2, 3, 4, 5)
    assert rpartial(f, 4, 5)(2, 3) == (2, 3, 4, 5)
    assert rpartial(f, 3, 4, 5)(2) == (2, 3, 4, 5)
import ast
import re
import operator
import inspect
import importlib
from functools import partial
from typing import Dict, Any, Optional, Union
from scanapi import std


_sentinel = object()


def get_module(name: str):
    """Import a module dynamically."""
    if name.lower() == 'std':
        return std
    module = importlib.import_module(name)
    print(f'Loaded {module}')
    return module


def getname(location: str, root) -> Any:
    """Get an ident's value from a given namespace."""
    trail = location.split('.')
    node = root
    for i, name in enumerate(trail):
        try:
            node = getattr(node, name)
        except AttributeError:
            raise AttributeError(f'No such location: {root}.{".".join(trail[:i + 1])}')
    return node


def unroll_name(name: Union[str, ast.Attribute, ast.Name]) -> str:
    """Unroll a ast.Name / ast.Attribute / str object."""
    if isinstance(name, str):
        return name
    if isinstance(name, ast.Name):
        return name.id
    return unroll_name(name.value) + '.' + name.attr


class RemoteMethodCallEvaluator:

    pattern = re.compile(
        r'^(?P<module>[\w.]*)\s*:\s*(?P<expr>.*)$'
    )

    @classmethod
    def evaluate(
        cls,
        code: str,
        vars: Dict[str, Any],
        is_a_test_case: bool = False,
        match: Optional[re.Match] = None
    ):
        """
        Parse a remote method call (rmc) expression, then run it against input `vars`.

        A rmc expression is made of two fields separated by a colon (:):
        * a module to import the function from: (eg 'pandas')
        * the name location of the function (eg 'is_nan')

        mymodule.py:

            def ok(response):
                return response.status_code == 200

            def status_is(code, response):
                return code == r esponse.status_code

        We can call this module's functions with rmc expressions.
        You can omit any and all arguments, but if you do provide some,
        they will be bound to the function before it gets to run.

        {{ mymodule:response.ok }}
        # with positional arguments
        {{ mymodule:response.status_is(200) }}
        # or keyword arguments
        {{ mymodule:response.status_is(code=200) }}

        Beware that partial binding binds from the left on positional arguments, so
        you should expect your positional arguments to be fed through the expression
        rather than from `vars`, ie don't write this but the above:

        ${{ mymodule:response.status_is(200) }}

        def status_is(response, code):  # response would be 200 here and a collision would happen
            ...

        `vars` is fed to the function as keyword arguments; only `vars` keys found in
        the function's spec are fed to the function, so you can write stuff like this:

        def analyze_response(response):
            ...

        with vars = {'response': ... , 'book_id': 333}
        ${{ !mymodule.analyze_response }}

        to just be able to process the vars you're interested in.
        """

        code = str(code)

        # Parse expr
        match = match or cls.pattern.match(code)
        if match is None:
            raise ValueError(
                "Failed to parse expr: %r" % code
            )

        modulename, callcode = match.groups()
        modulename = modulename or 'std'

        expr = ast.parse(callcode, mode='eval').body

        name = None
        args = None
        kwargs = None

        if isinstance(expr, ast.Call):
            name = unroll_name(expr.func)
            args = [ast.literal_eval(arg) for arg in expr.args]
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in expr.keywords}
        elif isinstance(expr, ast.Name):
            name = expr.id
        elif isinstance(expr, ast.Attribute):
            name = unroll_name(expr)
        else:
            raise ValueError(
                "Failed to parse %r as an attribute name or function call." % callcode
            )
        #

        # Build function
        module = get_module(modulename)
        func = getname(name, module)
        bound_func = func

        if args or kwargs:
            bound_func = partial(bound_func, *args or (), **kwargs or {})

        if getattr(func, '__module__', None) == 'builtins':
            result = bound_func(vars)
        else:
            spec = inspect.getfullargspec(func)
            result = bound_func(**{
                key: vars[key]
                for key in vars.keys() & {*spec.kwonlyargs, *spec.args}
            })

        if is_a_test_case:
            if operator.truth(result):
                return (True, None)
            return (False, code)

        return result

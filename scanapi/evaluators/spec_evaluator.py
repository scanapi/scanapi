import re
from collections.abc import KeysView, Sequence
from functools import singledispatch
from typing import Any

from scanapi.evaluators.string_evaluator import StringEvaluator


class SpecEvaluator:
    """Evaluate variables and assertions defined in the ScanAPI specification.

    This class maintains a registry of spec variables and evaluates
    expressions defined in the ScanAPI spec. It can also filter
    response-derived variables and supports evaluation of test case
    assertions.
    """

    def __init__(
        self,
        endpoint: Any,
        spec_vars: dict[str, Any],
        extras: dict[str, Any] | None = None,
        filter_responses: bool = True,
    ) -> None:
        """Initialize a SpecEvaluator.

        Args:
            endpoint (EndpointNode): Endpoint instance for which the
                spec is being evaluated.
            spec_vars (dict): Variables defined in the ScanAPI
                specification.
            extras (dict, optional): Optional extra variables to
                include in the registry.
            filter_responses (bool): Whether to filter out
                response-related variables.
        """
        self.endpoint = endpoint
        self.registry: dict[str, Any] = {}

        self.update(
            spec_vars,
            extras=extras,
            filter_responses=filter_responses,
        )

    def evaluate(self, element: Any) -> Any:
        """Evaluate a spec element.

        Args:
            element (Any): Spec element/expression to evaluate.

        Returns:
            Any: Evaluated value of the element.
        """
        return evaluate(element, self)

    def evaluate_assertion(self, element: Any) -> Any:
        """Evaluate an assertion element.

        Args:
            element (Any): Assertion expression from a test case.

        Returns:
            Any: Result of the evaluated assertion.
        """
        return _evaluate_str(element, self, is_a_test_case=True)

    def update(
        self,
        spec_vars: dict[str, Any],
        extras: dict[str, Any] | None = None,
        filter_responses: bool = False,
    ) -> None:
        """Update the evaluator registry with evaluated spec variables.

        This method evaluates each variable in ``spec_vars``
        (optionally using ``extras`` during evaluation) and updates
        the internal registry.

        Args:
            spec_vars (dict): Mapping of spec variable names to
                expressions/values.
            extras (dict, optional): Optional extra variables to
                include in the registry.
            filter_responses (bool): Whether to filter out
                response-related variables.
        """
        if extras is None:
            extras = {}

        if filter_responses:
            spec_vars = self.filter_response_var(spec_vars)

        values = {
            key: evaluate(value, extras) for key, value in spec_vars.items()
        }

        self.registry.update(extras)
        self.registry.update(values)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the registry.

        Args:
            key (str): Name of the variable to retrieve.
            default (Any): Value to return if the key does not exist.

        Returns:
            Any: Value associated with the given key or
                ``default`` if key is not present.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self) -> str:
        """Return a string representation of the evaluator registry."""
        return self.registry.__repr__()

    def __getitem__(self, key: str) -> Any:
        """Retrieve a variable value from the registry.

        Args:
            key (str): Variable name to retrieve.

        Returns:
            Any: Value for the given key.

        Raises:
            KeyError: If the key is not present in the registry or
                endpoint variables.
        """
        if key in self:
            return self.registry[key]

        all_vars = self.endpoint.get_all_vars()

        if key in all_vars:
            return all_vars[key]

        raise KeyError(key)

    def __delitem__(self, key: str) -> None:
        """Delete a variable from the registry.

        Args:
            key (str): Variable name to delete.

        Raises:
            KeyError: If the key is not present in the registry.
        """
        if key in self:
            del self.registry[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """Check whether a variable exists in the registry.

        Args:
            key (str): Variable name.

        Returns:
            bool: True if the variable exists in the registry,
                otherwise False.
        """
        return key in self.registry

    def keys(self) -> KeysView[str]:
        """Return a copy of the dictionary keys.

        Returns:
            KeysView[str]: The registry keys.
        """
        return self.registry.keys()

    @classmethod
    def filter_response_var(
        cls,
        spec_vars: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a copy of ``spec_vars`` without response references.

        Any items with a ``response.*`` reference in their value
        are left out.

        Returns:
            dict: Filtered dictionary.
        """
        pattern = re.compile(r"(?:(\s*response\.\w+))")

        return {
            key: value
            for key, value in spec_vars.items()
            if not pattern.search(value)
        }


@singledispatch
def evaluate(
    expression: Any,
    _spec_vars: Any,
) -> Any:
    """Evaluate a spec expression based on its type.

    This function is implemented using
    ``functools.singledispatch`` to support different types of
    expressions (e.g. strings, dictionaries, lists).

    Args:
        expression: Expression/value to evaluate.
        _spec_vars: SpecEvaluator instance or variable registry
            used during evaluation.

    Returns:
        Any: Evaluated result or original expression if no
            evaluation is needed.
    """
    return expression


@evaluate.register(str)
def _evaluate_str(
    element: str,
    spec_vars: Any,
    is_a_test_case: bool = False,
) -> Any:
    """Evaluate a string expression using the StringEvaluator.

    Args:
        element: String expression from the spec.
        spec_vars: SpecEvaluator instance or variable registry
            used during evaluation.
        is_a_test_case: Whether this evaluation is happening in
            a test case context.

    Returns:
        Any: Evaluated result of the string expression.
    """
    return StringEvaluator.evaluate(
        element,
        spec_vars,
        is_a_test_case,
    )


@evaluate.register(dict)
def _evaluate_dict(
    element: dict[str, Any],
    spec_vars: Any,
) -> dict[str, Any]:
    """Recursively evaluate dictionary values.

    Args:
        element: Dictionary containing expressions/values.
        spec_vars: SpecEvaluator instance or variable registry
            used during evaluation.

    Returns:
        dict: Dictionary with evaluated values.
    """
    return {key: evaluate(value, spec_vars) for key, value in element.items()}


@evaluate.register(list)
@evaluate.register(tuple)
def _evaluate_collection(
    elements: Sequence[Any],
    spec_vars: Any,
) -> list[Any]:
    """Recursively evaluate a list/tuple of spec expressions.

    Args:
        elements: List/tuple containing expressions/values.
        spec_vars: SpecEvaluator instance or variable registry
            used during evaluation.

    Returns:
        list: List with evaluated elements.
    """
    return [evaluate(item, spec_vars) for item in elements]

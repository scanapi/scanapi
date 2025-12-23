from httpx import Client, HTTPTransport

from scanapi.errors import InvalidKeyError, MissingMandatoryKeyError
from scanapi.tree.tree_keys import MAX_RETRIES_KEY


def join_urls(first_url, second_url):
    """Function that returns one url if two aren't given else joins the two
    urls and returns them.
    """
    if not first_url:
        return second_url

    if not second_url:
        return first_url

    first_url = first_url.strip("/")
    second_url = second_url.lstrip("/")

    return "/".join([first_url, second_url])


def validate_keys(keys, available_keys, required_keys, scope):
    """Caller function that validates keys."""
    _validate_allowed_keys(keys, available_keys, scope)
    _validate_required_keys(keys, required_keys, scope)


def _validate_allowed_keys(keys, available_keys, scope):
    """Private function that checks if the spec keys are allowed.

    Args:
        keys [list of strings]: the specification keys
        available_keys [tuple of string]: the available keys for that scope
        scope [string]: the scope of the current node: 'root', 'endpoint',
        'request' or 'test'

    """
    for key in keys:
        if key not in available_keys:
            raise InvalidKeyError(key, scope, available_keys)


def _validate_required_keys(keys, required_keys, scope):
    """Private function that checks if there is any required key missing.

    Args:
        keys [list of strings]: the specification keys
        required_keys [tuple of string]: the required keys for that scope
        scope [string]: the scope of the current node: 'root', 'endpoint',
        'request' or 'test'

    """
    if not set(required_keys) <= set(keys):
        missing_keys = set(required_keys) - set(keys)
        raise MissingMandatoryKeyError(missing_keys, scope)


def session_with_retry(retry_configuration, verify=True):
    """Instantiate a requests session.

    Args:
        retry_configuration [dict]: The retry configuration
        for a request. (Available for version >= 2.2.0).
        verify [bool]: SSL certificates used to verify the
        identity of requested hosts

    Returns:
        [httpx.Client]: Client
    """
    retry_configuration = retry_configuration or {}
    retries = retry_configuration.get(MAX_RETRIES_KEY, 0)

    return Client(
        transport=HTTPTransport(retries=retries), timeout=None, verify=verify
    )

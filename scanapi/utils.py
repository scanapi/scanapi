import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from scanapi.errors import InvalidKeyError, MissingMandatoryKeyError
from scanapi.tree.tree_keys import MAX_RETRIES_KEY


def join_urls(first_url, second_url):
    """Function that returns one url if two aren't given else joins the two urls and
    returns them.
    """
    if not first_url:
        return second_url

    if not second_url:
        return first_url

    first_url = first_url.strip("/")
    second_url = second_url.lstrip("/")

    return "/".join([first_url, second_url])


def validate_keys(keys, available_keys, required_keys, scope):
    """ Caller function that validates keys. """
    _validate_allowed_keys(keys, available_keys, scope)
    _validate_required_keys(keys, required_keys, scope)


def _validate_allowed_keys(keys, available_keys, scope):
    """ Private function that checks validation of allowed keys. """
    for key in keys:
        if key not in available_keys:
            raise InvalidKeyError(key, scope, available_keys)


def _validate_required_keys(keys, required_keys, scope):
    """ Private function that checks validation of required keys. """
    if not set(required_keys) <= set(keys):
        missing_keys = set(required_keys) - set(keys)
        raise MissingMandatoryKeyError(missing_keys, scope)


def session_with_retry(retry_configuration):
    """Instantiate a requests session with the retry configuration if provided by
    instantiating an HTTPAdapter mounting it into the mounting it into the
    `requests.Session`.
    """
    session = requests.Session()

    if not retry_configuration:
        return session

    retry = Retry(total=retry_configuration.get(MAX_RETRIES_KEY, 0))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

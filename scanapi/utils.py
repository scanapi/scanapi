from scanapi.errors import InvalidKeyError, MissingMandatoryKeyError


def join_urls(first_url, second_url):
    if not first_url:
        return second_url

    if not second_url:
        return first_url

    first_url = first_url.strip("/")
    second_url = second_url.lstrip("/")

    return "/".join([first_url, second_url])


def validate_keys(keys, available_keys, required_keys, scope):
    _validate_allowed_keys(keys, available_keys, scope)
    _validate_required_keys(keys, required_keys, scope)


def _validate_allowed_keys(keys, available_keys, scope):
    for key in keys:
        if not key in available_keys:
            raise InvalidKeyError(key, scope, available_keys)


def _validate_required_keys(keys, required_keys, scope):
    if not set(required_keys) <= set(keys):
        missing_keys = set(required_keys) - set(keys)
        raise MissingMandatoryKeyError(missing_keys, scope)

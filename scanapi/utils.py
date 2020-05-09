from scanapi.errors import InvalidKeyError
from scanapi.settings import settings

ALLOWED_ATTRS_TO_HIDE = ("headers body").split()


def join_urls(first_url, second_url):
    if not first_url:
        return second_url

    if not second_url:
        return first_url

    first_url = first_url.strip("/")
    second_url = second_url.lstrip("/")

    return "/".join([first_url, second_url])


def validate_keys(keys, available_keys, scope):
    for key in keys:
        if not key in available_keys:
            raise InvalidKeyError(key, scope, available_keys)


def hide_sensitive_info(response):
    report_settings = settings.get("report", {})
    request = response.request
    request_settings = report_settings.get("hide-request", {})
    response_settings = report_settings.get("hide-response", {})

    _hide(request, request_settings)
    _hide(response, response_settings)


def _hide(http_msg, hide_settings):
    for http_attr in hide_settings:
        secret_fields = hide_settings[http_attr]
        for field in secret_fields:
            _override_info(http_msg, http_attr, field)


def _override_info(http_msg, http_attr, secret_field):
    if (
        secret_field in getattr(http_msg, http_attr)
        and http_attr in ALLOWED_ATTRS_TO_HIDE
    ):
        getattr(http_msg, http_attr)[secret_field] = "<sensitive_information>"

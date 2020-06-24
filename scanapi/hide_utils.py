from scanapi.settings import settings

HEADERS = "headers"
BODY = "body"
URL = "url"

ALLOWED_ATTRS_TO_HIDE = (HEADERS, BODY, URL)
SENSITIVE_INFO_SUBSTITUTION_FLAG = "SENSITIVE_INFORMATION"


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
        if http_attr == URL:
            new_url = getattr(http_msg, http_attr).replace(
                secret_field, SENSITIVE_INFO_SUBSTITUTION_FLAG
            )
            setattr(http_msg, http_attr, new_url)
        else:
            getattr(http_msg, http_attr)[
                secret_field
            ] = SENSITIVE_INFO_SUBSTITUTION_FLAG

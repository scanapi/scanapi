import json
from json.decoder import JSONDecodeError
from urllib.parse import parse_qs, urlparse, urlunparse

from scanapi.settings import settings

HEADERS = "headers"
BODY = "body"
URL = "url"
PARAMS = "params"

SENSITIVE_INFO_SUBSTITUTION_FLAG = "SENSITIVE_INFORMATION"


def hide_sensitive_info(response):
    """Takes response and hides the sensitive data replacing the info with the
    string `SENSITIVE_INFORMATION`.

    Args:
        response [requests.models.Response]: the response that has
        information to be hidden.

    """
    report_settings = settings.get("report", {})
    request = response.request
    request_settings = report_settings.get("hide_request", {})
    response_settings = report_settings.get("hide_response", {})

    _hide(request, request_settings)
    _hide(response, response_settings)


def _hide(http_msg, hide_settings):
    """Private method that finds all sensitive information attributes and calls
    _override_info to have sensitive data replaced.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        hide_settings [dic]: the fields that need to be hidden for each http
        attribute (body, headers, url params)

    """
    for http_attr in hide_settings:
        secret_fields = hide_settings[http_attr]
        for field in secret_fields:
            _override_info(http_msg, http_attr, field)


def _override_info(http_msg, http_attr, secret_field):
    """Private method that substitutes sensitive data with string
    'SENSITIVE_INFORMATION'.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        http_attr [string]: the http_attr that has a field to be hidden: body,
        headers, url or params
        secret_field [string]: the secret field which its value must be hidden.

    """
    if http_attr == URL:
        _override_url(http_msg, secret_field)
    elif http_attr == HEADERS:
        _override_headers(http_msg, secret_field)
    elif http_attr == PARAMS:
        _override_params(http_msg, secret_field)
    elif http_attr == BODY:
        _override_body(http_msg, secret_field)


def _override_url(http_msg, secret_field):
    """Private method that substitutes sensitive data with string
    'SENSITIVE_INFORMATION' in URLs.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        secret_field [string]: the secret field which its value must be hidden
        in the URL.

    """
    url_parsed = urlparse(http_msg.url)
    if secret_field in url_parsed.path:
        new_url = url_parsed._replace(
            path=url_parsed.path.replace(
                secret_field, SENSITIVE_INFO_SUBSTITUTION_FLAG
            )
        )
        new_url = urlunparse(new_url)
        http_msg.url = new_url


def _override_headers(http_msg, secret_field):
    """Private method that substitutes sensitive data with string
    'SENSITIVE_INFORMATION' in the request/response headers.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        secret_field [string]: the secret field which its value must be hidden
        in the request/response headers.

    """
    if secret_field in http_msg.headers:
        http_msg.headers[secret_field] = SENSITIVE_INFO_SUBSTITUTION_FLAG


def _override_params(http_msg, secret_field):
    """Private method that substitutes sensitive data with string
    'SENSITIVE_INFORMATION' in the request/response params.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        secret_field [string]: the secret field which its value must be hidden
        in the request/response params.

    """
    url_parsed = urlparse(http_msg.url)
    query_parsed = parse_qs(url_parsed.query)
    param_values_list = query_parsed.get(secret_field, [])
    param_values_list.sort(key=len, reverse=True)

    for value in param_values_list:
        url_parsed = url_parsed._replace(
            query=url_parsed.query.replace(
                f"{secret_field}={value}",
                f"{secret_field}={SENSITIVE_INFO_SUBSTITUTION_FLAG}",
            )
        )

    new_url = urlunparse(url_parsed)
    http_msg.url = new_url


def _override_body(http_msg, secret_field):
    """Private method that substitutes sensitive data with string
    'SENSITIVE_INFORMATION' in the request/response body/content.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        secret_field [string]: the secret field which its value must be hidden
        in the request/response body/content.

    """
    body = _get_json_body(http_msg)

    if body and secret_field in body:
        body[secret_field] = SENSITIVE_INFO_SUBSTITUTION_FLAG
        _set_json_body(http_msg, body)


def _get_json_body(http_msg):
    """Private method that gets the json body/content of a request/response.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.

    Returns:
        [dict]: the json body/content of the request/response.

    """
    try:
        body = _get_body(http_msg)

        if not body:
            return None

        return json.loads(body)

    except JSONDecodeError:
        return None


def _get_body(http_msg):
    """Private method that gets the body/content of a request/response.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.

    Returns:
        [bytes]: the body/content of the request/response.
    """
    if not hasattr(http_msg, "body"):
        return http_msg._content

    return http_msg.body


def _set_json_body(http_msg, value):
    """Private method that sets the json body/content of a request/response.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        value [dict]: the json body/content of the request/response.

    """
    value = json.dumps(value).encode("utf-8")
    _set_body(http_msg, value)


def _set_body(http_msg, value):
    """Private method that sets the body/content of a request/response.

    Args:
        http_msg [requests.models.PreparedRequest / requests.models.Response]:
        the request or the response that has information to be hidden.
        value [bytes]: the body/content of the request/response.

    """
    if not hasattr(http_msg, "body"):
        http_msg._content = value
        return

    http_msg.body = value

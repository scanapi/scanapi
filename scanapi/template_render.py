"""Rendering and loading templates either from a directory
in the filesystem or scanapi.
"""

import curlify2
from jinja2 import Environment, FileSystemLoader, PackageLoader


def render(template_path, context, is_external=False):
    """Controller function that handles the Jinga2 rending of the template

    Args:
        template_path [string]: path to the report template
        context [dict]: values required to render template.
        is_external [bool, optional]: True for jinja2.FileSystemLoader otherwise jinja2.PackageLoader

    Returns:
        [html]: rendered report

    """
    loader = _loader(is_external)
    env = Environment(loader=loader)
    env.filters["curlify"] = curlify2.to_curl
    env.filters["render_body"] = render_body
    chosen_template = env.get_template(template_path)
    return chosen_template.render(**context)


def _loader(is_external):
    """Wrapper for jinja2 template loader method to get template from filesystem
    or package directory.

    Args:
        is_external [bool]: load an external template from a directory in the file system.

    Returns:
        [jinja2.FileSystemLoader or jinja2.PackageLoader]: template loading class.

    """
    if is_external:
        return FileSystemLoader(searchpath="./")

    return PackageLoader("scanapi", "templates")


def render_body(request):
    """Render body according to its request content type.

    Args:
        request [request object]: getting content type from request headers.

    Returns:
        [string]: content_type of the request.

    """
    content_type = request.headers.get("Content-Type")
    if content_type in ["application/json", "text/plain"]:
        return request.body.decode()
    elif content_type.startswith("application"):
        return "Binary content"

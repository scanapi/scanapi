import itertools

import curlify2
from jinja2 import Environment, FileSystemLoader, PackageLoader


def render(template_path, context, is_external=False):
    """Controller function that handles the Jinja2 rending of the template."""
    loader = _loader(is_external)
    env = Environment(
        loader=loader,
        autoescape=True,
        extensions=["jinja2_humanize_extension.HumanizeExtension"],
    )
    env.filters["curlify"] = curlify2.to_curl
    env.filters["render_body"] = render_body
    env.filters["group_by_child_endpoint"] = group_by_child_endpoints
    env.globals["is_bytes"] = lambda o: isinstance(o, bytes)
    chosen_template = env.get_template(template_path)
    return chosen_template.render(**context)


def _loader(is_external):
    """
    Private function that either returns Jinja2 FileSystemLoader or the
    PackageLoader.
    """
    if is_external:
        return FileSystemLoader(searchpath="./")

    return PackageLoader("scanapi", "templates")


def render_body(request):
    """Render body according to its request content type."""
    content_type = request.headers.get("Content-Type")
    if content_type in ["application/json", "text/plain"]:
        return request.body.decode()
    return f"Can not render. Unsuported content type: {content_type}."


def group_by_child_endpoints(results):
    """
    Groups results by endpoint name

    Args:
        [iterator]: iterator of request results

    Returns:
        [iterator]: an iterator with tuples containing the endpoint name
        and an iterator for all request results of that endpoint
    """

    def by_child_endpoint_name(result):
        endpoint_name = result["endpoint_name"]
        root, *generations = endpoint_name.split("::")
        return generations[0] if generations else root or "root"

    return itertools.groupby(results, by_child_endpoint_name)

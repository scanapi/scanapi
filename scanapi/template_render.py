import curlify2
from jinja2 import Environment, FileSystemLoader, PackageLoader


def render(template_path, context, is_external=False):
    """Controller function that handles the Jinja2 rending of the template."""
    loader = _loader(is_external)
    env = Environment(loader=loader, autoescape=True)
    env.filters["curlify"] = curlify2.to_curl
    env.filters["render_body"] = render_body
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

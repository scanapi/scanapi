import curlify

from jinja2 import Environment, FileSystemLoader, PackageLoader


def render(template_path, context, is_external=False):
    loader = _loader(is_external)
    env = Environment(loader=loader)
    env.filters["curlify"] = curlify.to_curl
    chosen_template = env.get_template(template_path)

    return chosen_template.render(**context)


def _loader(is_external):
    if is_external:
        return FileSystemLoader(searchpath="./")

    return PackageLoader("scanapi", "templates")

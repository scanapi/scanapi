name = "scanapi"

import click
import logging

from scanapi.tree.api_tree import APITree
from scanapi.docs_writer import ConsoleReporter, MarkdownReporter
from scanapi.requests_maker import RequestsMaker
from scanapi.settings import SETTINGS
from scanapi.yaml_loader import load_yaml


@click.command()
@click.option(
    "-s",
    "--spec-path",
    "spec_path",
    type=click.Path(exists=True),
    default=SETTINGS["spec_path"],
)
@click.option("-d", "--docs-path", "docs_path", default=SETTINGS["docs_path"])
@click.option(
    "--log-level",
    "log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
)
def scan(spec_path, docs_path, log_level):
    """Automated Testing and Documentation for your REST API."""

    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    SETTINGS.update({"spec_path": spec_path, "docs_path": docs_path})

    spec_path = SETTINGS["spec_path"]
    try:
        api_spec = load_yaml(spec_path)
    except FileNotFoundError as e:
        error_message = f"Could not find spec file: {spec_path}"
        logger.error(error_message)
        return

    try:
        api_tree = APITree(api_spec)
    except Exception as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        return

    responses = RequestsMaker(api_tree.leaves).make_all()
    MarkdownReporter(docs_path).write(responses)
    ConsoleReporter().write(responses)

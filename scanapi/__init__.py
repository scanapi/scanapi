name = "scanapi"

import click
import logging

from scanapi.docs_writer import DocsWriter
from scanapi.requests_builder import RequestsBuilder
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
        error_message = "Could not find spec file: {}".format(spec_path)
        logger.error(error_message)
        return

    try:
        request_builder = RequestsBuilder(api_spec)
    except Exception as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        return

    request_builder.build_all()
    responses = request_builder.call_all()
    DocsWriter(docs_path).write(responses)

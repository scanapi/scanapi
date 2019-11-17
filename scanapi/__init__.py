name = "scanapi"

import click
import logging

from scanapi.tree.api_tree import APITree
from scanapi.reporter import Reporter
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
@click.option("-o", "--output-path", "output_path")
@click.option(
    "-r",
    "--reporter",
    "reporter",
    type=click.Choice(["console", "markdown", "html"]),
    default=SETTINGS["reporter"],
)
@click.option("-t", "--template", "template")
@click.option(
    "--log-level",
    "log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
)
def scan(spec_path, output_path, reporter, template, log_level):
    """Automated Testing and Documentation for your REST API."""

    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    SETTINGS.update({"spec_path": spec_path, "output_path": output_path})

    # custom templates to be implemented later
    if template is not None:
        logger.warn("Custom templates are not supported yet. Soon to be. Hang tight.")

    spec_path = SETTINGS["spec_path"]
    try:
        api_spec = load_yaml(spec_path)
    except FileNotFoundError as e:
        error_message = f"Could not find spec file: {spec_path}. {str(e)}"
        logger.error(error_message)
        return

    try:
        api_tree = APITree(api_spec)
    except Exception as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        return

    RequestsMaker(api_tree).make_all()
    Reporter(output_path, reporter, template).write(api_tree.responses.values())

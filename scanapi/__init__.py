name = "scanapi"

import click
import logging
import yaml

from scanapi.errors import EmptyConfigFileError, InvalidKeyError
from scanapi.tree import EndpointNode
from scanapi.reporter import Reporter
from scanapi.settings import SETTINGS
from scanapi.config_loader import load_config_file


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
        api_spec = load_config_file(spec_path)
    except FileNotFoundError as e:
        error_message = f"Could not find API spec file: {spec_path}. {str(e)}"
        logger.error(error_message)
        return
    except EmptyConfigFileError as e:
        error_message = f"API spec file is empty. {str(e)}"
        logger.error(error_message)
        return
    except yaml.YAMLError as e:
        logger.error(e)
        return

    try:
        root_node = EndpointNode(api_spec["api"])
        Reporter(output_path, reporter, template).write(root_node.run())
    except InvalidKeyError as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        return

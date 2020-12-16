import logging

import click
import yaml

from scanapi.exit_code import ExitCode
from scanapi.scan import scan
from scanapi.settings import settings

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group()
def main():
    """
    Automated Testing and Documentation for your REST API.
    """
    pass


@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("spec_path", type=click.Path(exists=True), required=False)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    type=click.Path(),
    help="Report output path.",
)
@click.option(
    "-c",
    "--config-path",
    "config_path",
    type=click.Path(exists=True),
    help="Configuration file path.",
)
@click.option(
    "-t",
    "--template",
    "template",
    type=click.Path(exists=True),
    help="Custom report template path. The template must be a .jinja file.",
)
@click.option(
    "-ll",
    "--log-level",
    "log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the debug logging level for the program.",
)
def run(spec_path, output_path, config_path, template, log_level):
    """
    Automated Testing and Documentation for your REST API.
    SPEC_PATH argument is the API specification file path.
    """
    logging.basicConfig(level=log_level, format="%(message)s")
    logger = logging.getLogger(__name__)

    click_preferences = {
        "spec_path": spec_path,
        "output_path": output_path,
        "config_path": config_path,
        "template": template,
    }

    try:
        settings.save_preferences(**click_preferences)
    except yaml.YAMLError as e:
        error_message = "Error loading configuration file."
        error_message = "{}\nPyYAML: {}".format(error_message, str(e))
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)

    scan()

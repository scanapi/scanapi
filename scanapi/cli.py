import logging

import click
import yaml
from importlib.metadata import version
from rich.logging import RichHandler

from scanapi.exit_code import ExitCode
from scanapi.scan import scan
from scanapi.convert import openapi_to_scanapi
from scanapi.settings import settings

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def configure_logging(log_level):
    if logging.getLogger().handlers:
        return

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                show_time=False, markup=True, show_path=(log_level == "DEBUG")
            )
        ],
    )


def save_preferences(**click_preferences):
    logger = logging.getLogger(__name__)

    try:
        settings.save_preferences(**click_preferences)
    except yaml.YAMLError as e:
        logger.error(f"Error loading configuration file.\nPyYAML: {e}")
        raise SystemExit(ExitCode.USAGE_ERROR)


# -------------------
# Shared options
# -------------------
def log_level_option():
    return click.option(
        "-ll",
        "--log-level",
        type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
        default="INFO",
        help="Set the logging level.",
    )


def config_path_option():
    return click.option(
        "-c",
        "--config-path",
        type=click.Path(exists=True),
        help="Configuration file path. Default is scanapi.conf",
    )


# -------------------
# CLI root
# -------------------
@click.group()
@click.version_option(version=version("scanapi"))
def main():
    """Automated Testing and Documentation for your REST API."""


# -------------------
# RUN
# -------------------
@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("spec_path", type=click.Path(exists=True), required=False)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    type=click.Path(),
    help="Report output path. Default is scanapi-report.html",
)
@click.option(
    "-nr",
    "--no-report",
    "no_report",
    is_flag=True,
    help="Run ScanAPI without generating report.",
)
@click.option(
    "-b",
    "--browser",
    "open_browser",
    is_flag=True,
    help="Open the results file using a browser",
)
@click.option(
    "-t",
    "--template",
    "template",
    type=click.Path(exists=True),
    help="Custom report template path. The template must be a .jinja file.",
)
@config_path_option()
@log_level_option()
def run(
    spec_path,
    output_path,
    no_report,
    config_path,
    template,
    log_level,
    open_browser,
):
    """
    Automated Testing and Documentation for your REST API.
    """
    configure_logging(log_level)
    save_preferences(
        spec_path=spec_path,
        output_path=output_path,
        no_report=no_report,
        config_path=config_path,
        template=template,
        open_browser=open_browser,
    )
    scan()


# -------------------
# FROM
# -------------------
@main.group(name="from")
def from_():
    """Convert from other formats into ScanAPI"""


@from_.command(name="openapi", context_settings=CONTEXT_SETTINGS)
@click.argument(
    "input_path",
    metavar="OPENAPI_PATH",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "-b",
    "--base-url",
    "base_url",
    type=str,
    help="Base URL for the API.",
)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    type=click.Path(),
    help="Output ScanAPI file path (default: scanapi.yaml).",
)
@config_path_option()
@log_level_option()
def from_openapi(input_path, base_url, output_path, log_level, config_path):
    """
    Convert an OpenAPI document (JSON or YAML) into ScanAPI format.

    \b
    Arguments:
        OPENAPI_PATH: The OpenAPI file path (JSON or YAML).

    \b
    Examples:
      scanapi from openapi api.json
      scanapi from openapi api.yaml -o scanapi.yaml
    """
    configure_logging(log_level)
    save_preferences(
        input_path=input_path,
        base_url=base_url,
        output_path=output_path,
        config_path=config_path,
    )
    openapi_to_scanapi()

import logging

import click
import yaml
from importlib.metadata import version
from rich.logging import RichHandler

from scanapi.exit_code import ExitCode
from scanapi.openapi_to_scanapi import openapi_to_scanapi, get_openapi_specs
from scanapi.scan import scan
from scanapi.settings import settings

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group()
@click.version_option(version=version("scanapi"))
def main():
    """Automated Testing and Documentation for your REST API."""


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
    SPEC_PATH argument is the API specification file path.
    """
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
    logger = logging.getLogger(__name__)

    click_preferences = {
        "spec_path": spec_path,
        "output_path": output_path,
        "no_report": no_report,
        "config_path": config_path,
        "template": template,
        "open_browser": open_browser,
    }

    try:
        settings.save_preferences(**click_preferences)
    except yaml.YAMLError as e:
        error_message = "Error loading configuration file."
        error_message = f"{error_message}\nPyYAML: {e}"
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)

    scan()


@main.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-b",
    "--base-url",
    "base_url",
    type=str,
    help="Base URL for the API.",
    default="${BASE_URL}",
)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    default="scanapi.yaml",
    type=click.Path(),
    help="ScanAPI YAML output path.",
)
@click.argument("openapi_path", type=click.Path(exists=True), required=True)
def convert(openapi_path, base_url, output_path):
    """
    Converts a OpenAPI JSON file into a ScanAPI friendly YAML file.
    OPENAPI_PATH argument is the OpenAPI JSON file path.
    """
    specs = get_openapi_specs(openapi_path)
    scanapi_yaml = openapi_to_scanapi(specs, base_url)
    with open(output_path, "w") as file:
        yaml.dump(scanapi_yaml, file, default_flow_style=False, sort_keys=False, indent=4)
    print(f'File successfully converted and exported as "{output_path}"!')

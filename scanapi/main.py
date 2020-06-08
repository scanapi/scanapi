import click
import logging

from scanapi.scan import scan
from scanapi.settings import settings


@click.command()
@click.option("-s", "--spec-path", "spec_path", type=click.Path(exists=True))
@click.option("-o", "--output-path", "output_path", type=click.Path())
@click.option("-c", "--config-path", "config_path", type=click.Path(exists=True))
@click.option(
    "-r", "--reporter", "reporter", type=click.Choice(["console", "markdown", "html"])
)
@click.option("-t", "--template", "template", type=click.Path(exists=True))
@click.option(
    "--log-level",
    "log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
)
def main(spec_path, output_path, config_path, reporter, template, log_level):
    """Automated Testing and Documentation for your REST API."""
    logging.basicConfig(level=log_level, format="%(message)s")
    logger = logging.getLogger(__name__)

    click_preferences = {
        "spec_path": spec_path,
        "output_path": output_path,
        "config_path": config_path,
        "reporter": reporter,
        "template": template,
    }

    settings.save_preferences(**click_preferences)
    scan()

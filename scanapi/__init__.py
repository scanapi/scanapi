name = "scanapi"

from scanapi.docs_writer import DocsWriter
from scanapi.requests_builder import RequestsBuilder
from scanapi.settings import SETTINGS

import click


@click.command()
def scan():
    """Automated Testing and Documentation for your REST API."""

    responses = RequestsBuilder(SETTINGS["spec_path"]).all_responses()
    DocsWriter(SETTINGS["docs_path"]).write(responses)

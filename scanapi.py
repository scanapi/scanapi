from docs_writer import DocsWriter
from requests_builder import RequestsBuilder
from settings import SETTINGS

import click


@click.command()
def scan():
    """Automated Testing and Documentation for your REST API."""

    responses = RequestsBuilder(SETTINGS["spec_path"]).all_responses()
    DocsWriter(SETTINGS["docs_path"]).write(responses)


if __name__ == "__main__":
    scan()

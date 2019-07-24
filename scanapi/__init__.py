name = "scanapi"

from scanapi.docs_writer import DocsWriter
from scanapi.requests_builder import RequestsBuilder
from scanapi.settings import SETTINGS

import click


@click.command()
@click.option('-s', '--spec-path', 'spec_path', type=click.Path(exists=True), default=SETTINGS['spec_path'])
@click.option('-d', '--docs-path', 'docs_path', default=SETTINGS['docs_path'])
def scan(spec_path, docs_path):
    """Automated Testing and Documentation for your REST API."""

    SETTINGS.update({'spec_path': spec_path, 'docs_path': docs_path})

    responses = RequestsBuilder(spec_path).all_responses()
    DocsWriter(docs_path).write(responses)

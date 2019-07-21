from docs_writer import DocsWriter
from requests_builder import RequestsBuilder
from settings import SETTINGS

if __name__ == "__main__":
    responses = RequestsBuilder(SETTINGS["api-file"]).all_responses()
    DocsWriter(SETTINGS["docs-file"]).write(responses)

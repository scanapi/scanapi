from requests_builder import RequestsBuilder
from docs_writer import DocsWriter


if __name__ == "__main__":
    responses = RequestsBuilder("api.yaml").all_responses()
    DocsWriter("docs.md").write(responses)

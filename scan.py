import os
import yaml

from requests_builder import RequestsBuilder
from docs_writer import DocsWriter

CONFIG_FILE = ".api-scanner.yaml"
DEFAULT_CONFIG = {"api-file": "api.yaml", "docs-file": "docs.md"}


def config():
    if not os.path.isfile(CONFIG_FILE):
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as stream:
        try:
            user_config = yaml.safe_load(stream)
            return {**DEFAULT_CONFIG, **user_config}
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    config = config()
    responses = RequestsBuilder(config["api-file"]).all_responses()
    DocsWriter(config["docs-file"]).write(responses)

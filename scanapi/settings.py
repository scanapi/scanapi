import os
import yaml

SETTINGS_FILE = ".scanapi.yaml"
DEFAULT_SETTINGS = {"spec_path": "api.yaml", "docs_path": "docs.md"}


def settings():
    if not os.path.isfile(SETTINGS_FILE):
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as stream:
        try:
            user_config = yaml.safe_load(stream)
            return {**DEFAULT_SETTINGS, **user_config}
        except yaml.YAMLError as exc:
            print(exc)


SETTINGS = settings()

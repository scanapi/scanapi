import os
from scanapi.yaml_loader import load_yaml

SETTINGS_FILE = ".scanapi.yaml"
DEFAULT_SETTINGS = {"spec_path": "api.yaml", "docs_path": "docs.md"}


def settings():
    if not os.path.isfile(SETTINGS_FILE):
        return DEFAULT_SETTINGS

    user_config = load_yaml(SETTINGS_FILE)
    return {**DEFAULT_SETTINGS, **user_config}


SETTINGS = settings()

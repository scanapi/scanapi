import os

from scanapi.config_loader import load_config_file

SETTINGS_FILE = ".scanapi.yaml"
DEFAULT_SETTINGS = {"spec_path": "api.yaml", "reporter": "markdown"}


def settings():
    if not os.path.isfile(SETTINGS_FILE):
        return DEFAULT_SETTINGS

    user_config = load_config_file(SETTINGS_FILE)
    return {**DEFAULT_SETTINGS, **user_config}


SETTINGS = settings()

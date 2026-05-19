import os

import appdirs

from scanapi.config_loader import load_config_file

GLOBAL_CONFIG_PATH = os.path.join(
    appdirs.site_config_dir("scanapi"),
    "scanapi.conf",
)

LOCAL_CONFIG_PATH = "./scanapi.conf"
DEFAULT_SETTINGS = {
    "spec_path": "scanapi.yaml",
    "output_path": None,
    "template": None,
    "no_report": False,
    "open_browser": False,
    "input_path": None,
    "base_url": "${BASE_URL}",
}


class Settings(dict):
    """Class for generating Settings dictionary."""

    def __init__(self):
        """
        Constructs a Settings object with default values for all possible preferences.
        """
        super().__init__()
        self.update(DEFAULT_SETTINGS)

    def save_config_file_preferences(self, config_path=None):
        """Saves the Settings object config file preferences."""
        path = None

        if config_path:
            path = config_path
        elif self.has_local_config_file:
            path = LOCAL_CONFIG_PATH
        elif self.has_global_config_file:
            path = GLOBAL_CONFIG_PATH

        if path:
            self["config_path"] = path
            self.update(**load_config_file(path))

    def save_click_preferences(self, **preferences):
        """Saves all preference items to the Settings object."""
        cleaned_preferences = {
            k: v for k, v in preferences.items() if v is not None
        }
        self.update(**cleaned_preferences)

    def save_preferences(self, **click_preferences):
        """Caller function that begins the saving of Setting preferences."""
        config_path = click_preferences.get("config_path")
        self.save_config_file_preferences(config_path)
        self.save_click_preferences(**click_preferences)

    @property
    def has_global_config_file(self):
        """Checks if there is a global config file."""
        return os.path.isfile(GLOBAL_CONFIG_PATH)

    @property
    def has_local_config_file(self):
        """Checks if there is a local config file."""
        return os.path.isfile(LOCAL_CONFIG_PATH)


settings = Settings()

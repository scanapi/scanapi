import os

from scanapi.config_loader import load_config_file

DEFAULT_CONFIG_PATH = ".scanapi.yaml"


class Settings(dict):
    """ Class for generating Settings dictionary. """

    def __init__(self):
        """ Constructs a Settings object with dictionary keys spec_path, output_path and template. """
        self["spec_path"] = "scanapi.yaml"
        self["output_path"] = None
        self["template"] = None

        super(dict, self).__init__()

    def save_config_file_preferences(self, config_path=None):
        """ Saves the Settings object config file preferences. """
        if not config_path and not self.has_default_config_file:
            return

        if not config_path:
            user_config = load_config_file(DEFAULT_CONFIG_PATH)
            self["config_path"] = DEFAULT_CONFIG_PATH
            self.update(**user_config)
            return

        user_config = load_config_file(config_path)
        self.update(**user_config)

    def save_click_preferences(self, **preferences):
        """ Saves all preference items to the Settings object. """
        cleaned_preferences = {k: v for k, v in preferences.items() if v is not None}
        self.update(**cleaned_preferences)

    def save_preferences(self, **click_preferences):
        """ Caller function that begins the saving of Setting preferences. """
        config_path = (
            click_preferences["config_path"]
            if "config_path" in click_preferences
            else None
        )
        self.save_config_file_preferences(config_path)
        self.save_click_preferences(**click_preferences)

    @property
    def has_default_config_file(self):
        """ Helper property that returns whether the default config path exists. """
        return os.path.isfile(DEFAULT_CONFIG_PATH)


settings = Settings()

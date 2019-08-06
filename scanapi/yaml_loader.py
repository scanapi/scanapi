import logging
import yaml

logger = logging.getLogger(__name__)


def load_yaml(file_path):
    with open(file_path, "r") as stream:
        try:
            logger.info("Loading file {}".format(file_path))
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logger.error(e)

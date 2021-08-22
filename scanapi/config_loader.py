"""Code Reference https://gist.github.com/joshbode/569627ced3076931b02f"""

import logging
import os
from typing import IO, Any

import yaml

from scanapi.errors import BadConfigIncludeError, EmptyConfigFileError

logger = logging.getLogger(__name__)


class Loader(yaml.SafeLoader):
    """YAML/JSON Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""
        try:
            self.root = os.path.split(stream.name)[0]
        except AttributeError:
            self.root = os.path.curdir

        super().__init__(stream)


def construct_include(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    if not isinstance(node, yaml.ScalarNode):
        include_node_str = yaml.serialize(node).strip()
        message = f"Include tag value is not a scalar: {include_node_str}"
        raise BadConfigIncludeError(message)
    include_file_path = str(loader.construct_scalar(node))
    relative_path = os.path.join(loader.root, include_file_path)
    full_path = os.path.abspath(relative_path)

    with open(full_path) as f:
        return yaml.load(f, Loader)


def load_config_file(file_path):
    """
    Loads configuration file. If non-empty file exists reads data and
    returns it.
    """
    with open(file_path, "r") as stream:
        logger.info(f"Loading file {file_path}")
        data = yaml.load(stream, Loader)

        if not data:
            raise EmptyConfigFileError(file_path)

        return data


yaml.add_constructor("!include", construct_include, Loader)

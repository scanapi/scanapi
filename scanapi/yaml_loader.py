"""
Code based on solution https://gist.github.com/joshbode/569627ced3076931b02f
"""

import logging
import yaml

import os
import json
from typing import Any, IO

from scanapi.errors import EmptySpecError

logger = logging.getLogger(__name__)


class Loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)


def construct_include(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""

    filename = os.path.abspath(
        os.path.join(loader._root, loader.construct_scalar(node))
    )
    extension = os.path.splitext(filename)[1].lstrip(".")

    with open(filename, "r") as f:
        if extension in ("yaml", "yml"):
            return yaml.load(f, Loader)
        elif extension in ("json",):
            return json.load(f)
        else:
            return "".join(f.readlines())


yaml.add_constructor("!include", construct_include, Loader)


def load_yaml(file_path):
    with open(file_path, "r") as stream:
        logger.info(f"Loading file {file_path}")
        data = yaml.load(stream, Loader)

        if not data:
            raise EmptySpecError

        return data

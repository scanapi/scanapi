import logging
import sys
import yaml

from scanapi.config_loader import load_config_file
from scanapi.errors import (
    BadConfigurationError,
    EmptyConfigFileError,
    FileFormatNotSupportedError,
    InvalidKeyError,
    InvalidPythonCodeError,
    MissingMandatoryKeyError,
)
from scanapi.exit_code import ExitCode
from scanapi.reporter import Reporter
from scanapi.session import session
from scanapi.settings import settings
from scanapi.tree import EndpointNode
from scanapi.tree.tree_keys import API_KEY, ROOT_SCOPE

logger = logging.getLogger(__name__)


def scan():
    spec_path = settings["spec_path"]

    try:
        api_spec = load_config_file(spec_path)
    except FileNotFoundError as e:
        error_message = f"Could not find API spec file: {spec_path}. {str(e)}"
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)
    except EmptyConfigFileError as e:
        error_message = f"API spec file is empty. {str(e)}"
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)
    except (yaml.YAMLError, FileFormatNotSupportedError) as e:
        logger.error(e)
        raise SystemExit(ExitCode.USAGE_ERROR)

    try:
        if API_KEY not in api_spec:
            raise MissingMandatoryKeyError({API_KEY}, ROOT_SCOPE)

        root_node = EndpointNode(api_spec[API_KEY])
        results = root_node.run()

    except (
        InvalidKeyError,
        MissingMandatoryKeyError,
        KeyError,
        InvalidPythonCodeError,
    ) as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)

    try:
        write_report(results)
    except (BadConfigurationError, InvalidPythonCodeError) as e:
        logger.error(e)
        raise SystemExit(ExitCode.USAGE_ERROR)

    session.exit()


def write_report(results):
    reporter = Reporter(settings["output_path"], settings["template"])
    reporter.write(results)

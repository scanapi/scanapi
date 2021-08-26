import logging

import yaml

from scanapi.config_loader import load_config_file
from scanapi.errors import (
    BadConfigurationError,
    EmptyConfigFileError,
    InvalidKeyError,
    InvalidPythonCodeError,
)
from scanapi.exit_code import ExitCode
from scanapi.reporter import Reporter
from scanapi.session import session
from scanapi.settings import settings
from scanapi.tree import EndpointNode

logger = logging.getLogger(__name__)


def scan():
    """Caller function that tries to scans the file and write the report."""
    spec_path = settings["spec_path"]
    no_report = settings["no_report"]
    open_browser = settings["open_browser"]

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
    except yaml.YAMLError as e:
        error_message = "Error loading specification file."
        error_message = "{}\nPyYAML: {}".format(error_message, str(e))
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)

    try:
        root_node = EndpointNode(api_spec)
        results = root_node.run()

    except (InvalidKeyError, KeyError, InvalidPythonCodeError,) as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)

    if no_report:
        write_without_generating_report(results)
    else:
        try:
            write_report(results)
            if open_browser:
                open_report_in_browser()
        except (BadConfigurationError, InvalidPythonCodeError) as e:
            logger.error(e)
            raise SystemExit(ExitCode.USAGE_ERROR)

    session.exit()


def write_report(results):
    """Constructs a Reporter object and calls the write method of Reporter to
    push the results to a file.
    """
    reporter = Reporter(settings["output_path"], settings["template"])
    reporter.write(results)


def open_report_in_browser():
    """Open the results file on a browser"""
    reporter = Reporter(settings["output_path"], settings["template"])
    reporter.open_report_in_browser()


def write_without_generating_report(results):
    """Constructs a Reporter object and calls the
    write_without_generating_report method of Reporter to print the results to
    the console output without generating a report.
    """
    reporter = Reporter()
    reporter.write_without_generating_report(results)

import logging

import yaml

from scanapi.config_loader import load_config_file
from scanapi.console import write_results, write_summary
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

    except (
        InvalidKeyError,
        KeyError,
        InvalidPythonCodeError,
    ) as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        raise SystemExit(ExitCode.USAGE_ERROR)

    _write(results)
    write_summary()
    session.exit()


def _write(results):
    """When the user passed the `--no-report` flag: prints the test results to
    the console output.
    When the user did not pass the `--no_report flag`: writes the results on a
    report file and opens it using a browser, if the --browser flag is present.

    Returns:
        None
    """
    no_report = settings["no_report"]
    open_browser = settings["open_browser"]

    if no_report:
        write_results(results)
        return

    try:
        _write_report(results, open_browser)
    except (BadConfigurationError, InvalidPythonCodeError) as e:
        logger.error(e)
        raise SystemExit(ExitCode.USAGE_ERROR)


def _write_report(results, open_browser):
    """Constructs a Reporter object and calls the write method of Reporter to
    push the results to a file.

    Returns:
        None
    """
    reporter = Reporter(settings["output_path"], settings["template"])
    reporter.write(results, open_browser)

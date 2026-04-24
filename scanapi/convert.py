import logging
from typing import cast

import prance
import yaml
from rich.console import Console
from ruamel.yaml import scanner

from scanapi.converters.from_openapi import OpenAPIToScanAPIConverter
from scanapi.settings import settings

logger = logging.getLogger(__name__)
console = Console()


def openapi_to_scanapi():
    """Caller function that tries to convert the specification file and write the report.

    Uses [prance](https://github.com/RonnyPfannschmidt/prance) for resolving
    and parsing the OpenAPI schema.

    Returns:
        None
    """
    openapi_path = settings["input_path"]
    base_url = settings["base_url"]
    output_path = settings["output_path"]

    logger.info(
        f"Loading file [deep_sky_blue1 underline]{openapi_path}",
        extra={"highlighter": None},
    )

    try:
        parser = prance.ResolvingParser(openapi_path)
    except scanner.ScannerError as e:
        error_message = f"Couldn't parse received yaml file: {str(e)}"
        logger.error(error_message)
        raise SystemExit(1)
    except AttributeError as e:
        error_message = f"Couldn't parse received json file: {str(e)}"
        logger.error(error_message)
        raise SystemExit(1)
    except prance.ValidationError as e:
        error_message = "Invalid OpenAPI schema.\n"
        error_message += "Conversion currently requires a valid OpenAPI 3.x document.\n"
        error_message += f"Details: {str(e)}"
        logger.error(error_message)
        raise SystemExit(1)

    parser.parse()
    openapi_spec = cast(dict, parser.specification)
    converter = OpenAPIToScanAPIConverter(openapi_spec)
    scanapi_yaml, created_variables = converter.convert(base_url)
    with open(output_path, "w") as file:
        yaml.dump(
            scanapi_yaml,
            file,
            default_flow_style=False,
            sort_keys=False,
            indent=4,
        )
    console.print(
        f"File successfully converted and exported as [deep_sky_blue1 underline]{output_path}"
    )
    if len(created_variables) > 0:
        console.print(
            "\nThe following variables were created in the generated ScanAPI YAML file:"
        )
        for variable in created_variables:
            console.print("- ${" + variable + "}")
        console.print(
            "\nSee [deep_sky_blue1 underline]https://scanapi.dev/docs_v1/specification/custom_variables[/deep_sky_blue1 underline]"
            "\nand [deep_sky_blue1 underline]https://scanapi.dev/docs_v1/specification/environment_variables[/deep_sky_blue1 underline]"
            "\nfor more information."
        )

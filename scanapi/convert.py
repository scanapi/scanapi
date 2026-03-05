import logging

import prance
from typing import cast
from scanapi.openapi_converter import OpenAPIConverter
import yaml
from ruamel.yaml import scanner
from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()


def convert(openapi_path: str, base_url: str, output_path: str) -> None:
    """Caller function that tries to convert the specification file and write the report.

    Uses [prance](https://github.com/RonnyPfannschmidt/prance) for resolving
    and parsing the OpenAPI schema.
    
    Returns:
        None
    """
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
    except prance.ValidationError as e:
        error_message = f"Couldn't parse OpenAPI schema: {str(e)}"
        logger.error(error_message)
        raise SystemExit(1)

    parser.parse()
    openapi_spec = cast(dict, parser.specification)
    converter = OpenAPIConverter(openapi_spec)
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
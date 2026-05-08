from scanapi.convert import openapi_to_scanapi
from scanapi.settings import settings
import logging
from pytest import mark, raises


@mark.describe("openapi_to_scanapi")
@mark.describe("openapi_to_scanapi")
class TestOpenAPIToScanAPI:
    @mark.context("when called with an openapi_path")
    @mark.it("should call the resolving parser on the openapi_path")
    def test_call_resolving_parser_on_path(self, mocker):
        parser_mock = mocker.Mock()

        parser_mock.parse.return_value = None
        parser_mock.specification = {"openapi": "3.0.4"}

        mock_resolving_parser = mocker.patch(
            "scanapi.convert.prance.ResolvingParser", return_value=parser_mock
        )

        mocker.patch("scanapi.convert.yaml.dump")
        mocker.patch("builtins.open", mocker.mock_open())

        settings["input_path"] = "openapi.json"
        settings["base_url"] = "$BASE_URL"
        settings["output_path"] = "scanapi.yaml"

        openapi_to_scanapi()
        mock_resolving_parser.assert_called_once_with("openapi.json")

    @mark.context("when the convertion runs successfully")
    @mark.it("should write to the output_path")
    def test_writes_to_output_path(self, mocker):
        parser_mock = mocker.Mock()

        parser_mock.parse.return_value = None
        parser_mock.specification = {"openapi": "3.0.4"}

        mocker.patch(
            "scanapi.convert.prance.ResolvingParser", return_value=parser_mock
        )
        converter_mock = mocker.Mock()
        converter_mock.convert.return_value = {"test": "test"}, set()

        mocker.patch(
            "scanapi.convert.OpenAPIToScanAPIConverter",
            return_value=converter_mock,
        )

        yaml_dump_mock = mocker.patch("scanapi.convert.yaml.dump")
        open_mock = mocker.patch("builtins.open", mocker.mock_open())

        settings["input_path"] = "openapi.json"
        settings["base_url"] = "$BASE_URL"
        settings["output_path"] = "test.yaml"

        openapi_to_scanapi()
        open_mock.assert_called_once_with("test.yaml", "w")
        yaml_dump_mock.assert_called_once_with(
            {"test": "test"},
            open_mock(),
            default_flow_style=False,
            sort_keys=False,
            indent=4,
        )

    @mark.context("when the convertion generates created_variables")
    @mark.it("should print the variables to the console")
    def test_prints_created_variables(self, mocker, capsys):
        parser_mock = mocker.Mock()

        parser_mock.parse.return_value = None
        parser_mock.specification = {"openapi": "3.0.4"}

        mocker.patch(
            "scanapi.convert.prance.ResolvingParser", return_value=parser_mock
        )
        converter_mock = mocker.Mock()
        converter_mock.convert.return_value = (
            {"test": "test"},
            {"one", "two", "three"},
        )

        mocker.patch(
            "scanapi.convert.OpenAPIToScanAPIConverter",
            return_value=converter_mock,
        )

        mocker.patch("scanapi.convert.yaml.dump")
        mocker.patch("builtins.open", mocker.mock_open())

        settings["input_path"] = "openapi.json"
        settings["base_url"] = "$BASE_URL"
        settings["output_path"] = "test.yaml"

        openapi_to_scanapi()
        captured = capsys.readouterr()

        assert "The following variables were created" in captured.out
        assert "${one}" in captured.out
        assert "${two}" in captured.out
        assert "${three}" in captured.out

    @mark.context("when the openapi_path points to an invalid yaml file")
    @mark.it("should log an error")
    def test_handles_invalid_yaml_file(self, caplog):
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                settings["input_path"] = "tests/data/convert/invalid.yaml"
                settings["base_url"] = "$BASE_URL"
                settings["output_path"] = "scanapi.yaml"
                openapi_to_scanapi()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 1

    @mark.context("when the openapi_path points to an invalid json file")
    @mark.it("should log an error")
    def test_handles_invalid_json_file(self, caplog):
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                settings["input_path"] = "tests/data/convert/invalid.json"
                settings["base_url"] = "$BASE_URL"
                settings["output_path"] = "scanapi.yaml"
                openapi_to_scanapi()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 1

    @mark.context("when the openapi_path points to an empty json file")
    @mark.it("should log an error")
    def test_handles_empty_json_file(self, caplog):
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                settings["input_path"] = "tests/data/convert/empty.json"
                settings["base_url"] = "$BASE_URL"
                settings["output_path"] = "scanapi.yaml"
                openapi_to_scanapi()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 1

    @mark.context(
        "when the openapi_path points to a schema without version definition"
    )
    @mark.it("should log an error")
    def test_handles_invalid_openapi_schema(self, caplog):
        with caplog.at_level(logging.ERROR):
            with raises(SystemExit) as excinfo:
                settings["input_path"] = "tests/data/convert/no_version_definition.yaml"
                settings["base_url"] = "$BASE_URL"
                settings["output_path"] = "scanapi.yaml"
                openapi_to_scanapi()

            assert excinfo.type == SystemExit
            assert excinfo.value.code == 1

            assert "Invalid OpenAPI schema" in caplog.text

from pytest import fixture, mark

from scanapi.openapi_converter import OpenAPIConverter


@mark.describe("openapi converter")
@mark.describe("__init__")
class TestInit:
    @fixture
    def mock_get_openapi_specs(self, mocker):
        return mocker.patch.object(
            OpenAPIConverter,
            "_get_openapi_specs",
            return_value={"openapi": "3.0.0"},
        )

    @fixture
    def mock_validate_version(self, mocker):
        return mocker.patch.object(
            OpenAPIConverter, "_validate_openapi_spec_version"
        )

    @mark.it("should call _get_openapi_specs with the given path")
    def test_calls_get_openapi_specs(
        self, mock_get_openapi_specs, mock_validate_version
    ):
        OpenAPIConverter("some/path.yaml")
        mock_get_openapi_specs.assert_called_once_with("some/path.yaml")

    @mark.it("should call _validate_openapi_spec_version")
    def test_calls_validate_version(
        self, mock_get_openapi_specs, mock_validate_version
    ):
        OpenAPIConverter("some/path.yaml")
        mock_validate_version.assert_called_once()

    @mark.it("should initialize created_variables as an empty set")
    def test_initializes_created_variables(
        self, mock_get_openapi_specs, mock_validate_version
    ):
        converter = OpenAPIConverter("some/path.yaml")
        assert converter.created_variables == set()

    @mark.it("should assign specs from _get_openapi_specs")
    def test_assigns_specs(self, mock_get_openapi_specs, mock_validate_version):
        converter = OpenAPIConverter("some/path.yaml")
        assert converter.specs == {"openapi": "3.0.0"}

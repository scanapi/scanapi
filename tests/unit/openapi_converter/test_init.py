from pytest import fixture, mark

from scanapi.openapi_converter import OpenAPIConverter


@mark.describe("openapi converter")
@mark.describe("__init__")
class TestInit:
    @fixture
    def mock_validate_version(self, mocker):
        return mocker.patch.object(
            OpenAPIConverter, "_validate_openapi_spec_version"
        )

    @mark.it("should call _validate_openapi_spec_version")
    def test_calls_validate_version(self, mock_validate_version):
        OpenAPIConverter({"openapi": "3.0.0"})
        mock_validate_version.assert_called_once()

    @mark.it("should initialize created_variables as an empty set")
    def test_initializes_created_variables(self, mock_validate_version):
        converter = OpenAPIConverter({"openapi": "3.0.0"})
        assert converter.created_variables == set()

    @mark.it("should assign specs from received value")
    def test_assigns_specs(self, mock_validate_version):
        converter = OpenAPIConverter({"openapi": "3.0.0"})
        assert converter.specs == {"openapi": "3.0.0"}

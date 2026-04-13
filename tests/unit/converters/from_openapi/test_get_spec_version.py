from pytest import fixture, mark, raises

from scanapi.converters.from_openapi import OpenAPIToScanAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIToScanAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi to scanapi converter")
@mark.describe("_get_spec_version")
class TestGetSpecVersion:
    @mark.context("when spec has 'openapi' key")
    @mark.it("should return the openapi version string")
    def test_returns_openapi_version(self, converter):
        converter.specs = {"openapi": "3.0.0"}
        assert converter._get_spec_version() == "3.0.0"

    @mark.context("when spec has 'swagger' key")
    @mark.it("should return the swagger version string")
    def test_returns_swagger_version(self, converter):
        converter.specs = {"swagger": "2.0"}
        assert converter._get_spec_version() == "2.0"

    @mark.context("when spec has both 'openapi' and 'swagger' keys")
    @mark.it("should prefer the 'openapi' key")
    def test_prefers_openapi_key(self, converter):
        converter.specs = {"openapi": "3.1.0", "swagger": "2.0"}
        assert converter._get_spec_version() == "3.1.0"

    @mark.context("when spec has neither 'openapi' nor 'swagger' keys")
    @mark.it("should raise ValueError")
    def test_raises_value_error(self, converter):
        converter.specs = {"info": {"title": "My API"}}
        with raises(ValueError) as excinfo:
            converter._get_spec_version()
        assert (
            "Could not determine OpenAPI/Swagger specification version"
            in str(excinfo.value)
        )

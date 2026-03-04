from pytest import fixture, mark

from scanapi.openapi_converter import OpenAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi converter")
@mark.describe("_get_security_schemes")
class TestGetSecuritySchemes:
    @mark.context("when spec has no components key")
    @mark.it("should return an empty list")
    def test_no_components(self, converter):
        converter.specs = {"openapi": "3.0.0"}
        assert converter._get_security_schemes() == []

    @mark.context("when spec components has no securitySchemes key")
    @mark.it("should return an empty list")
    def test_no_security_schemes_key(self, converter):
        converter.specs = {"components": {"schemas": {}}}
        assert converter._get_security_schemes() == []

    @mark.context("when spec has a bearer http security scheme")
    @mark.it("should return the scheme with name and scheme=bearer")
    def test_http_bearer_scheme(self, converter):
        converter.specs = {
            "components": {
                "securitySchemes": {
                    "BearerAuth": {"type": "http", "scheme": "bearer"}
                }
            }
        }
        result = converter._get_security_schemes()
        assert result == [{"name": "BearerAuth", "scheme": "bearer"}]

    @mark.context("when spec has a basic http security scheme")
    @mark.it("should return the scheme with name and scheme=basic")
    def test_http_basic_scheme(self, converter):
        converter.specs = {
            "components": {
                "securitySchemes": {
                    "BasicAuth": {"type": "http", "scheme": "basic"}
                }
            }
        }
        result = converter._get_security_schemes()
        assert result == [{"name": "BasicAuth", "scheme": "basic"}]

    @mark.context("when spec has an oauth2 security scheme")
    @mark.it("should default scheme to bearer")
    def test_oauth2_scheme(self, converter):
        converter.specs = {
            "components": {
                "securitySchemes": {
                    "OAuth2": {
                        "type": "oauth2",
                        "flows": {"authorizationCode": {}},
                    }
                }
            }
        }
        result = converter._get_security_schemes()
        assert result == [{"name": "OAuth2", "scheme": "bearer"}]

    @mark.context("when spec has an unsupported security scheme type")
    @mark.it("should skip it and return empty list")
    def test_unsupported_scheme_type(self, converter):
        converter.specs = {
            "components": {
                "securitySchemes": {
                    "ApiKey": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-API-Key",
                    }
                }
            }
        }
        assert converter._get_security_schemes() == []

    @mark.context("when spec has multiple security schemes")
    @mark.it("should return all supported ones")
    def test_multiple_schemes(self, converter):
        converter.specs = {
            "components": {
                "securitySchemes": {
                    "BearerAuth": {"type": "http", "scheme": "bearer"},
                    "ApiKey": {"type": "apiKey"},
                    "BasicAuth": {"type": "http", "scheme": "basic"},
                }
            }
        }
        result = converter._get_security_schemes()
        assert len(result) == 2
        assert {"name": "BearerAuth", "scheme": "bearer"} in result
        assert {"name": "BasicAuth", "scheme": "basic"} in result

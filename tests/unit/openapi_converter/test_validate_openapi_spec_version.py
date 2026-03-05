from pytest import fixture, mark, raises

from scanapi.openapi_converter import OpenAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi converter")
@mark.describe("_validate_openapi_spec_version")
class TestValidateOpenAPISpecVersion:
    @mark.context("when spec version starts with '3'")
    @mark.it("should not raise")
    def test_valid_version_3(self, converter, mocker):
        mocker.patch.object(
            converter, "_get_spec_version", return_value="3.0.0"
        )
        converter._validate_openapi_spec_version()  # should not raise

    @mark.context("when spec version is '3.1.0'")
    @mark.it("should not raise")
    def test_valid_version_3_1(self, converter, mocker):
        mocker.patch.object(
            converter, "_get_spec_version", return_value="3.1.0"
        )
        converter._validate_openapi_spec_version()  # should not raise

    @mark.context("when spec version starts with '2'")
    @mark.it("should raise ValueError")
    def test_invalid_version_2(self, converter, mocker):
        mocker.patch.object(converter, "_get_spec_version", return_value="2.0")
        with raises(ValueError) as excinfo:
            converter._validate_openapi_spec_version()
        assert "OpenAPI/Swagger version 3 is required" in str(excinfo.value)

    @mark.context("when spec version starts with '1'")
    @mark.it("should raise ValueError")
    def test_invalid_version_1(self, converter, mocker):
        mocker.patch.object(converter, "_get_spec_version", return_value="1.2")
        with raises(ValueError) as excinfo:
            converter._validate_openapi_spec_version()
        assert "OpenAPI/Swagger version 3 is required" in str(excinfo.value)

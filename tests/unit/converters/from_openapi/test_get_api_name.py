from pytest import fixture, mark

from scanapi.converters.from_openapi import OpenAPIToScanAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIToScanAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi to scanapi converter")
@mark.describe("_get_api_name")
class TestGetApiName:
    @mark.context("when spec has info with title")
    @mark.it("should return the title")
    def test_returns_title(self, converter):
        converter.specs = {"info": {"title": "My API"}}
        assert converter._get_api_name() == "My API"

    @mark.context("when spec has no info key")
    @mark.it("should return None")
    def test_no_info_key(self, converter):
        converter.specs = {"openapi": "3.0.0"}
        assert converter._get_api_name() is None

    @mark.context("when spec info has no title key")
    @mark.it("should return None")
    def test_no_title_key(self, converter):
        converter.specs = {"info": {"version": "1.0.0"}}
        assert converter._get_api_name() is None

    @mark.context("when title is a non-string value")
    @mark.it("should return it as a string")
    def test_non_string_title(self, converter):
        converter.specs = {"info": {"title": 42}}
        assert converter._get_api_name() == "42"

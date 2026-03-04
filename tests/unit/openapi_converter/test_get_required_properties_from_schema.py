from pytest import fixture, mark

from scanapi.openapi_converter import OpenAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi converter")
@mark.describe("_get_required_properties_from_schema")
class TestGetRequiredPropertiesFromSchema:
    @mark.context("when schema has no required key")
    @mark.it("should return None")
    def test_no_required_key(self, converter):
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        result = converter._get_required_properties_from_schema(
            schema, "create_user"
        )
        assert result is None

    @mark.context("when schema has required properties")
    @mark.it("should return a dict with variable placeholders")
    def test_with_required_properties(self, converter):
        schema = {
            "type": "object",
            "required": ["username", "password"],
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
        }
        result = converter._get_required_properties_from_schema(
            schema, "create_user"
        )
        assert result == {
            "username": "${create_user_username}",
            "password": "${create_user_password}",
        }

    @mark.context("when schema has required properties")
    @mark.it("should add variables to created_variables")
    def test_adds_to_created_variables(self, converter):
        schema = {
            "type": "object",
            "required": ["username", "password"],
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
        }
        converter._get_required_properties_from_schema(schema, "register")
        assert len(converter.created_variables) == 2
        assert "register_username" in converter.created_variables
        assert "register_password" in converter.created_variables

    @mark.context("when schema has an empty required list")
    @mark.it("should return an empty dict")
    def test_empty_required_list(self, converter):
        schema = {"type": "object", "required": []}
        result = converter._get_required_properties_from_schema(
            schema, "create_user"
        )
        assert result == {}

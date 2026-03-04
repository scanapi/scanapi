from pytest import fixture, mark

from scanapi.openapi_converter import OpenAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi converter")
@mark.describe("_add_variables_to_path")
class TestAddVariablesToPath:
    @mark.context("when there are no parameters")
    @mark.it("should return the path unchanged")
    def test_no_params_path_unchanged(self, converter):
        result = converter._add_variables_to_path("/users", [], "list_users")
        assert result == "/users"

    @mark.context("when there are no parameters")
    @mark.it("shouldn't add anything to the created_variables")
    def test_no_params_created_variables_unchanged(self, converter):
        converter._add_variables_to_path("/users", [], "list_users")
        assert len(converter.created_variables) == 0

    @mark.context("when there is a path parameter")
    @mark.it("should replace curly braces with scanapi variable notation")
    def test_path_param(self, converter):
        params = [{"name": "id", "in": "path"}]
        result = converter._add_variables_to_path(
            "/users/{id}", params, "get_user"
        )
        assert result == "/users/${get_user_id}"

    @mark.context("when there is a path parameter")
    @mark.it("should add the variable to created_variables")
    def test_path_param_adds_variable(self, converter):
        params = [{"name": "id", "in": "path"}]
        converter._add_variables_to_path("/users/{id}", params, "get_user")
        assert "get_user_id" in converter.created_variables

    @mark.context("when there is a query parameter")
    @mark.it("shouldn't add anything to the created_variables")
    def test_ignore_query_param_created_variables(self, converter):
        params = [{"name": "search", "in": "query"}]
        converter._add_variables_to_path("/users", params, "list_users")
        assert len(converter.created_variables) == 0

    @mark.context("when there is a query parameter")
    @mark.it("should return the path unchanged")
    def test_ignores_query_param_path(self, converter):
        params = [{"name": "search", "in": "query"}]
        result = converter._add_variables_to_path(
            "/users", params, "list_users"
        )
        assert result == "/users"

    @mark.context("when there are both path and query parameters")
    @mark.it("should replace only path parameters")
    def test_replaces_only_path_params_when_mixed_params(self, converter):
        params = [
            {"name": "id", "in": "path"},
            {"name": "format", "in": "query"},
        ]
        result = converter._add_variables_to_path(
            "/users/{id}", params, "get_user"
        )
        assert result == "/users/${get_user_id}"

    @mark.context("when there are both path and query parameters")
    @mark.it("should add only path parameters to created_variables")
    def test_add_only_path_params_when_mixed_params(self, converter):
        params = [
            {"name": "id", "in": "path"},
            {"name": "format", "in": "query"},
        ]
        converter._add_variables_to_path("/users/{id}", params, "get_user")
        assert len(converter.created_variables) == 1
        assert "get_user_id" in converter.created_variables

    @mark.context("when there are multiple path parameters")
    @mark.it("should replace all of them")
    def test_replaces_multiple_path_params(self, converter):
        params = [
            {"name": "org_id", "in": "path"},
            {"name": "repo_id", "in": "path"},
        ]
        result = converter._add_variables_to_path(
            "/orgs/{org_id}/repos/{repo_id}", params, "get_repo"
        )
        assert result == "/orgs/${get_repo_org_id}/repos/${get_repo_repo_id}"

    @mark.context("when there are multiple path parameters")
    @mark.it("should add all the variable to created_variables")
    def test_adds_multiple_path_params_to_created_variables(self, converter):
        params = [
            {"name": "org_id", "in": "path"},
            {"name": "repo_id", "in": "path"},
        ]
        converter._add_variables_to_path(
            "/orgs/{org_id}/repos/{repo_id}", params, "get_repo"
        )
        assert len(converter.created_variables) == 2
        assert "get_repo_repo_id" in converter.created_variables
        assert "get_repo_org_id" in converter.created_variables

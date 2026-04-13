from pytest import mark

from scanapi.converters.from_openapi import get_api_target_name


@mark.describe("get_api_target_name")
class TestGetApiTargetName:
    @mark.context("when operation has a summary")
    @mark.it("should use summary, replacing spaces with underscores")
    def test_uses_summary(self):
        operation = {"summary": "List all users"}
        assert (
            get_api_target_name(operation, "/users", "get") == "List_all_users"
        )

    @mark.context("when operation has no summary but has operationId")
    @mark.it("should use operationId")
    def test_uses_operation_id(self):
        operation = {"operationId": "listUsers"}
        assert get_api_target_name(operation, "/users", "get") == "listUsers"

    @mark.context("when operation has both summary and operationId")
    @mark.it("should prefer summary over operationId")
    def test_prefers_summary_over_operation_id(self):
        operation = {"summary": "List users", "operationId": "listUsers"}
        assert get_api_target_name(operation, "/users", "get") == "List_users"

    @mark.context("when operation has neither summary nor operationId")
    @mark.it("should fall back to method_path")
    def test_fallback_to_method_path(self):
        assert get_api_target_name({}, "/users", "get") == "get__users"

    @mark.context("when the name contains slashes")
    @mark.it("should replace slashes with underscores")
    def test_replaces_slashes(self):
        operation = {"operationId": "get/users/active"}
        assert (
            get_api_target_name(operation, "/users", "get")
            == "get_users_active"
        )

    @mark.context("when the name contains spaces")
    @mark.it("should replace spaces with underscores")
    def test_replaces_spaces(self):
        operation = {"summary": "Get user by id"}
        assert (
            get_api_target_name(operation, "/users/{id}", "get")
            == "Get_user_by_id"
        )

    @mark.context("when the name is a non-string value")
    @mark.it("should return it as a string")
    def test_converts_to_string(self):
        operation = {"summary": 123}
        assert get_api_target_name(operation, "/users/{id}", "get") == "123"

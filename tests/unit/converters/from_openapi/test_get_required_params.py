from pytest import mark

from scanapi.converters.from_openapi import get_required_params


@mark.describe("get_required_params")
class TestGetRequiredParams:
    @mark.context("when operation has no parameters key")
    @mark.it("should return an empty list")
    def test_no_parameters_key(self):
        assert get_required_params({}) == []

    @mark.context("when operation has no required parameters")
    @mark.it("should return an empty list")
    def test_no_required_params(self):
        operation = {
            "parameters": [
                {"name": "search", "in": "query", "required": False},
                {"name": "page", "in": "query"},
            ]
        }
        assert get_required_params(operation) == []

    @mark.context("when operation has required parameters")
    @mark.it("should return them with name and in fields")
    def test_required_params(self):
        operation = {
            "parameters": [
                {"name": "id", "in": "path", "required": True},
                {"name": "search", "in": "query", "required": False},
            ]
        }
        result = get_required_params(operation)
        assert result == [{"name": "id", "in": "path"}]

    @mark.context("when all parameters are required")
    @mark.it("should return all of them")
    def test_all_required(self):
        operation = {
            "parameters": [
                {"name": "org_id", "in": "path", "required": True},
                {"name": "repo_id", "in": "path", "required": True},
            ]
        }
        result = get_required_params(operation)
        assert len(result) == 2
        assert {"name": "org_id", "in": "path"} in result
        assert {"name": "repo_id", "in": "path"} in result

    @mark.context("when parameters list is empty")
    @mark.it("should return an empty list")
    def test_empty_parameters(self):
        assert get_required_params({"parameters": []}) == []

    @mark.context("when a parameter has no name")
    @mark.it("should not be added to the list")
    def test_parameters_without_name(self):
        operation = {
            "parameters": [
                {"in": "path", "required": True},
                {"name": "repo_id", "in": "path", "required": True},
            ]
        }
        result = get_required_params(operation)
        assert len(result) == 1
        assert {"name": "repo_id", "in": "path"} in result

    @mark.context("when a parameter has no in key")
    @mark.it("should not be added to the list")
    def test_parameters_without_in(self):
        operation = {
            "parameters": [
                {"name": "org_id", "in": "path", "required": True},
                {"name": "repo_id", "required": True},
            ]
        }
        result = get_required_params(operation)
        assert len(result) == 1
        assert {"name": "org_id", "in": "path"} in result

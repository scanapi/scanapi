from pytest import mark

from scanapi.converters.from_openapi import get_tests


@mark.describe("get_tests")
class TestGetTests:
    @mark.context("when operation has no responses key")
    @mark.it("should return an empty list")
    def test_no_responses_key(self):
        assert get_tests({}) == []

    @mark.context("when operation has non-numeric response codes like '2XX'")
    @mark.it("should skip them")
    def test_non_numeric_status_code(self):
        operation = {"responses": {"2XX": {"description": "Success"}}}
        assert get_tests(operation) == []

    @mark.context("when operation has no 2xx responses")
    @mark.it("should return an empty list")
    def test_no_2xx_responses(self):
        operation = {
            "responses": {
                "400": {"description": "Bad Request"},
                "404": {"description": "Not Found"},
            }
        }
        assert get_tests(operation) == []

    @mark.context("when operation has a 200 response")
    @mark.it("should return a test asserting status_code == 200")
    def test_200_response(self):
        operation = {"responses": {"200": {"description": "OK"}}}
        result = get_tests(operation)
        assert result == [
            {
                "name": "status_code_is_200",
                "assert": "${{response.status_code == 200}}",
            }
        ]

    @mark.context("when operation has a 201 response")
    @mark.it("should return a test asserting status_code == 201")
    def test_201_response(self):
        operation = {"responses": {"201": {"description": "Created"}}}
        result = get_tests(operation)
        assert result == [
            {
                "name": "status_code_is_201",
                "assert": "${{response.status_code == 201}}",
            }
        ]

    @mark.context("when operation has multiple 2xx responses")
    @mark.it("should return a test for each")
    def test_multiple_2xx_responses(self):
        operation = {
            "responses": {
                "200": {"description": "OK"},
                "201": {"description": "Created"},
            }
        }
        result = get_tests(operation)
        assert len(result) == 2

    @mark.context("when operation has both 2xx and non-2xx responses")
    @mark.it("should return tests only for 2xx ones")
    def test_mixed_responses(self):
        operation = {
            "responses": {
                "200": {"description": "OK"},
                "400": {"description": "Bad Request"},
                "500": {"description": "Server Error"},
            }
        }
        result = get_tests(operation)
        assert len(result) == 1
        assert result[0]["name"] == "status_code_is_200"

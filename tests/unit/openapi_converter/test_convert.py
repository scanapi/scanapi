from pytest import fixture, mark

from scanapi.openapi_converter import OpenAPIConverter


@fixture
def converter():
    instance = object.__new__(OpenAPIConverter)
    instance.created_variables = set()
    return instance


@mark.describe("openapi converter")
@mark.describe("convert")
class TestConvert:
    @mark.context("when spec has no paths")
    @mark.it("should return base yaml with empty requests list")
    def test_no_paths(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
        }
        result = converter.convert("https://api.example.com")
        assert result == {
            "endpoints": [
                {
                    "name": "My API",
                    "path": "https://api.example.com",
                    "requests": [],
                }
            ]
        }

    @mark.context("when spec has an empty paths object")
    @mark.it("should return base yaml with empty requests list")
    def test_empty_paths(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {},
        }
        result = converter.convert("https://api.example.com")
        assert result == {
            "endpoints": [
                {
                    "name": "My API",
                    "path": "https://api.example.com",
                    "requests": [],
                }
            ]
        }

    @mark.context("when spec has a simple GET endpoint")
    @mark.it("should include it in requests")
    def test_simple_get_endpoint(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {
                "/users": {
                    "get": {
                        "operationId": "list_users",
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        requests = result["endpoints"][0]["requests"]
        assert len(requests) == 1
        assert requests[0]["name"] == "list_users"
        assert requests[0]["path"] == "/users"
        assert requests[0]["method"] == "get"

    @mark.context("when operation has non-HTTP method keys like 'parameters'")
    @mark.it("should skip them")
    def test_skips_non_http_method_keys(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {
                "/users": {
                    "parameters": [{"name": "X-Header", "in": "header"}],
                    "get": {
                        "operationId": "list_users",
                        "responses": {},
                    },
                }
            },
        }
        result = converter.convert("https://api.example.com")
        requests = result["endpoints"][0]["requests"]
        assert len(requests) == 1
        assert requests[0]["method"] == "get"

    @mark.context("when operation has a request body with required properties")
    @mark.it("should include body in the request")
    def test_request_with_body(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {
                "/users": {
                    "post": {
                        "operationId": "create_user",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["username"],
                                        "properties": {
                                            "username": {"type": "string"}
                                        },
                                    }
                                }
                            }
                        },
                        "responses": {"201": {"description": "Created"}},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        request = result["endpoints"][0]["requests"][0]
        assert request["body"] == {"username": "${create_user_username}"}

    @mark.context("when operation has security with a known bearer scheme")
    @mark.it("should add Authorization Bearer header")
    def test_bearer_security_header(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "components": {
                "securitySchemes": {
                    "BearerAuth": {"type": "http", "scheme": "bearer"}
                }
            },
            "paths": {
                "/users": {
                    "get": {
                        "operationId": "list_users",
                        "security": [{"BearerAuth": []}],
                        "responses": {},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        request = result["endpoints"][0]["requests"][0]
        assert request["headers"] == {"Authorization": "Bearer ${bearer_token}"}
        assert "bearer_token" in converter.created_variables

    @mark.context("when operation has security with a known basic scheme")
    @mark.it("should add Authorization Basic header")
    def test_basic_security_header(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "components": {
                "securitySchemes": {
                    "BasicAuth": {"type": "http", "scheme": "basic"}
                }
            },
            "paths": {
                "/users": {
                    "get": {
                        "operationId": "list_users",
                        "security": [{"BasicAuth": []}],
                        "responses": {},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        request = result["endpoints"][0]["requests"][0]
        assert request["headers"] == {
            "Authorization": "Basic ${basic_auth_token}"
        }
        assert "basic_auth_token" in converter.created_variables

    @mark.context("when operation has a path parameter")
    @mark.it("should replace path parameter with scanapi variable")
    def test_path_parameter_replaced(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {
                "/users/{id}": {
                    "get": {
                        "operationId": "get_user",
                        "parameters": [
                            {"name": "id", "in": "path", "required": True}
                        ],
                        "responses": {},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        request = result["endpoints"][0]["requests"][0]
        assert request["path"] == "/users/${get_user_id}"

    @mark.context("when requestBody has no required properties")
    @mark.it("should not include body in the request")
    def test_no_body_when_no_required_properties(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {
                "/users": {
                    "post": {
                        "operationId": "create_user",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "nickname": {"type": "string"}
                                        },
                                    }
                                }
                            }
                        },
                        "responses": {},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        request = result["endpoints"][0]["requests"][0]
        assert "body" not in request

    @mark.context("when requestBody has multiple content types")
    @mark.it("should prefer application/x-www-form-urlencoded")
    def test_prefers_form_urlencoded_content_type(self, converter):
        converter.specs = {
            "openapi": "3.0.0",
            "info": {"title": "My API"},
            "paths": {
                "/login": {
                    "post": {
                        "operationId": "login",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "required": ["json_field"],
                                        "properties": {
                                            "json_field": {"type": "string"}
                                        },
                                    }
                                },
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "required": ["form_field"],
                                        "properties": {
                                            "form_field": {"type": "string"}
                                        },
                                    }
                                },
                            }
                        },
                        "responses": {},
                    }
                }
            },
        }
        result = converter.convert("https://api.example.com")
        request = result["endpoints"][0]["requests"][0]
        assert request["body"] == {"form_field": "${login_form_field}"}

import pytest
from pytest_bdd import scenario, given, when, then

from scanapi.requests_builder import RequestsBuilder


@pytest.fixture(autouse=True)
def mock_request(mocker):
    return mocker.patch("scanapi.requests_builder.requests.request")


@pytest.fixture
def api_spec():
    return {"api": {"base_url": "", "requests": [{"name": "", "method": ""}]}}


@scenario(
    "call_requests.feature",
    "API spec with only base_url and one request with name and method",
)
def test_call_requests():
    pass


@given("base_url is correct", target_fixture="api_spec")
def base_url(api_spec):
    api_spec["api"]["base_url"] = "https://jsonplaceholder.typicode.com/todos"
    return api_spec


@given("HTTP method is GET", target_fixture="api_spec")
def http_method(api_spec):
    api_spec["api"]["requests"][0]["method"] = "get"
    return api_spec


@then("the request should be made")
def get_called(api_spec, mock_request):
    request_builder = RequestsBuilder(api_spec)
    request_builder.build_all()
    request_builder.call_all()

    mock_request.assert_called_once_with(
        "GET",
        "https://jsonplaceholder.typicode.com/todos",
        headers={},
        params={},
        json={},
    )

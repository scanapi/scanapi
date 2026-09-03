import json
from unittest.mock import MagicMock

from scanapi.mcp.server import run

def test_run_serializes_response(mocker):
    # Mock settings and run_scan
    mocker.patch("scanapi.mcp.server.settings.save_preferences")
    mocker.patch("scanapi.mcp.server.write_output")
    mock_run_scan = mocker.patch("scanapi.mcp.server.run_scan")
    
    # Create a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://httpbin.org/health/"
    mock_response.request.method = "GET"
    mock_response.elapsed.total_seconds.return_value = 0.5
    mock_response.text = '{"status": "ok"}'

    # Create a mock test status
    class MockStatus:
        name = "PASSED"

    mock_results = [
        {
            "request_node_name": "health_check",
            "endpoint_name": "health",
            "no_failure": True,
            "response": mock_response,
            "tests_results": [
                {
                    "name": "status is 200",
                    "status": MockStatus(),
                    "failure": None,
                }
            ],
        }
    ]
    mock_run_scan.return_value = mock_results

    # Mock session
    mock_session = mocker.patch("scanapi.mcp.server.session")
    mock_session.successes = 1
    mock_session.failures = 0
    mock_session.errors = 0
    mock_session.succeed = True

    # Call run
    result = run(spec_path="dummy.yaml", no_report=True)

    # Validate output
    assert "summary" in result
    assert "results" in result
    
    # Assert serialization worked
    serialized_results = result["results"]
    assert len(serialized_results) == 1
    
    req_result = serialized_results[0]
    assert req_result["request_node_name"] == "health_check"
    
    resp = req_result["response"]
    assert resp["status_code"] == 200
    assert resp["url"] == "https://httpbin.org/health/"
    assert resp["method"] == "GET"
    assert resp["elapsed"] == 0.5
    assert resp["text"] == '{"status": "ok"}'
    
    test_results = req_result["tests_results"]
    assert len(test_results) == 1
    assert test_results[0]["name"] == "status is 200"
    assert test_results[0]["status"] == "PASSED"
    
    # Ensure it's JSON serializable
    json.dumps(result)

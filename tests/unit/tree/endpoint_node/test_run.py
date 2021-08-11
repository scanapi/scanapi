import logging

from pytest import fixture, mark

from scanapi.exit_code import ExitCode
from scanapi.tree import EndpointNode

log = logging.getLogger(__name__)


@mark.describe("endpoint node")
@mark.describe("run")
class TestRun:
    @fixture
    def mock_run_request(self, mocker):
        return mocker.patch("scanapi.tree.request_node.RequestNode.run")

    @fixture
    def mock_session(self, mocker):
        return mocker.patch("scanapi.tree.endpoint_node.session")

    @mark.context("when requests are successful")
    @mark.it("should return the responses of the requests")
    def test_when_requests_are_successful(self, mock_run_request):

        mock_run_request.side_effect = ["foo", "bar"]

        node = EndpointNode(
            {
                "endpoints": [
                    {
                        "name": "foo",
                        "requests": [
                            {"name": "First", "path": "http://foo.com/first",},
                            {
                                "name": "Second",
                                "path": "http://foo.com/second",
                            },
                        ],
                    }
                ],
                "name": "node",
                "requests": [],
            }
        )

        requests_gen = node.run()

        requests = []

        for request in requests_gen:
            requests.append(request)

        assert len(requests) == 2

        assert requests == ["foo", "bar"]

    @mark.context("when there is an error during a request")
    @mark.it("should log the error and change session exit code")
    def test_when_request_fails(self, mock_run_request, mock_session, caplog):

        mock_run_request.side_effect = ["foo", Exception("error: bar")]

        node = EndpointNode(
            {
                "endpoints": [
                    {
                        "name": "foo",
                        "requests": [
                            {"name": "First", "path": "http://foo.com/first",},
                            {
                                "name": "Second",
                                "path": "http://foo.com/second",
                            },
                        ],
                    }
                ],
                "name": "node",
                "requests": [],
            }
        )

        requests = []
        with caplog.at_level(logging.ERROR):
            requests_gen = node.run()

            for request in requests_gen:
                requests.append(request)

        assert len(requests) == 1

        assert (
            "\nError to make request `http://foo.com/second`. \nerror: bar\n"
            in caplog.text
        )

        assert mock_run_request.call_count == 2

        assert mock_session.exit_code == ExitCode.REQUEST_ERROR

import httpx
import pytest

from scanapi.tools.curl import convert_httpx_request_to_curl

@pytest.mark.asyncio
async def test_something_async(httpx_mock):
    httpx_mock.add_response(json={"name": "picachu"})

    async with httpx.AsyncClient() as client:
        response = await client.get("http://pokemon/1")
        result = convert_httpx_request_to_curl(response.request)
        assert result == ('curl -X GET -H "host: pokemon" -H "accept: */*" -H "accept-encoding: gzip, '
 'deflate" -H "connection: keep-alive" -H "user-agent: python-httpx/0.15.5" -d '
 "'' http://pokemon/1 --compressed")
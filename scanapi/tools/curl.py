import httpx

def convert_httpx_request_to_curl(request: httpx.request) -> str:
    body = request.read().decode()
    headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
    headers = " -H ".join(headers)
    return  f"curl -X {request.method} -H {headers} -d '{body}' {request.url} --compressed"
class MalformedSpecError(Exception):
    pass


class HTTPMethodNotAllowedError(MalformedSpecError):
    """Raised when the HTTP method in the API spec is invalid"""

    def __init__(self, method, allowed_methos, *args):
        message = "HTTP method not supported: {}. Supported methods: {}.".format(
            method, allowed_methos
        )
        super(HTTPMethodNotAllowedError, self).__init__(message, *args)


class APIKeyMissingError(MalformedSpecError):
    """Raised when `api` key is not specified at root scope in the API spec"""

    def __init__(self, *args):
        message = "Missing api `key` at root scope in the API spec"
        super(APIKeyMissingError, self).__init__(message, *args)

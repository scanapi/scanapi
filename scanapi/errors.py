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


class BadConfigurationError(Exception):
    """Raised when an environment variable was not set or was badly configured"""

    def __init__(self, env_var, *args):
        super(BadConfigurationError, self).__init__(
            "{} environment variable not set or badly configured".format(env_var), *args
        )

class MalformedSpecError(Exception):
    pass


class HTTPMethodNotAllowedError(MalformedSpecError):
    """Raised when the HTTP method in the API spec is invalid"""

    def __init__(self, method, allowed_methos, *args):
        message = (
            f"HTTP method not supported: {method}. Supported methods: {allowed_methos}."
        )
        super(HTTPMethodNotAllowedError, self).__init__(message, *args)


class APIKeyMissingError(MalformedSpecError):
    """Raised when 'api' key is not specified at root scope in the API spec"""

    def __init__(self, *args):
        message = "Missing api 'key' at root scope in the API spec"
        super(APIKeyMissingError, self).__init__(message, *args)


class InvalidKeyError(MalformedSpecError):
    """Raised when an invalid key is specified in the API spec"""

    def __init__(self, key, scope, available_keys, *args):
        message = f"Invalid key '{key}' at '{scope}' scope. Available keys are: {available_keys}"
        super(InvalidKeyError, self).__init__(message, *args)


class InvalidPythonCodeError(MalformedSpecError):
    """Raised when python code defined in the API spec raises an error"""

    def __init__(self, error_message, *args):
        error_message = f"Invalid Python code defined in the API spec: {error_message}"
        super(InvalidPythonCodeError, self).__init__(error_message, *args)


class BadConfigurationError(Exception):
    """Raised when an environment variable was not set or was badly configured"""

    def __init__(self, env_var, *args):
        super(BadConfigurationError, self).__init__(
            f"{env_var} environment variable not set or badly configured", *args
        )


class EmptyConfigFileError(Exception):
    """Raised when the Config File loaded is empty"""

    def __init__(self, file_path, *args):
        message = f"File '{file_path}' is empty."
        super(EmptyConfigFileError, self).__init__(message, *args)


class FileFormatNotSupportedError(Exception):
    """Raised when the Config File format is not supported"""

    def __init__(self, file_format, file_path, *args):
        message = f"The format {file_format} is not supported. Supported formats: '.yaml', '.yml', '.json'. File path: '{file_path}'."
        super(FileFormatNotSupportedError, self).__init__(message, *args)

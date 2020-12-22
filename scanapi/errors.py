class MalformedSpecError(Exception):
    pass


class HTTPMethodNotAllowedError(MalformedSpecError):
    """Raised when the HTTP method in the API spec is invalid"""

    def __init__(self, method, allowed_methods, *args):
        message = f"HTTP method not supported: {method}. Supported methods: {allowed_methods}."
        super(HTTPMethodNotAllowedError, self).__init__(message, *args)


class InvalidKeyError(MalformedSpecError):
    """Raised when an invalid key is specified in the API spec"""

    def __init__(self, key, scope, available_keys, *args):
        message = f"Invalid key '{key}' at '{scope}' scope. Available keys are: {available_keys}"
        super(InvalidKeyError, self).__init__(message, *args)


class MissingMandatoryKeyError(MalformedSpecError):
    """Raised when one or more mandatory keys are missing"""

    def __init__(self, missing_keys, scope, *args):
        missing_keys_str = ", ".join(f"'{k}'" for k in sorted(missing_keys))
        message = f"Missing {missing_keys_str} key(s) at '{scope}' scope"
        super(MissingMandatoryKeyError, self).__init__(message, *args)


class InvalidPythonCodeError(MalformedSpecError):
    """Raised when python code defined in the API spec raises an error"""

    def __init__(self, error_message, code, *args):
        error_message = (
            f"Invalid Python code defined in the API spec. "
            f"Exception: {error_message}. "
            f"Code: {code}."
        )
        super(InvalidPythonCodeError, self).__init__(error_message, *args)


class BadConfigurationError(Exception):
    """Raised when an environment variable was not set or was badly configured"""

    def __init__(self, env_var, *args):
        super(BadConfigurationError, self).__init__(
            f"{env_var} environment variable not set or badly configured",
            *args,
        )


class EmptyConfigFileError(Exception):
    """Raised when the Config File loaded is empty"""

    def __init__(self, file_path, *args):
        message = f"File '{file_path}' is empty."
        super(EmptyConfigFileError, self).__init__(message, *args)

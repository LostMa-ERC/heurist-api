class APIException(Exception):
    """Problem calling Heurist API."""


class AuthenticationError(Exception):
    """Error raised when unable to authenticate Heurist login."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MissingParameterException(Exception):
    """Exception raised for a missing parameter."""

    def __init__(self, parameter: str, env_file: str):
        self.message = f"Missing parameter: {parameter}\nTried looking at: {env_file}"
        super().__init__(self.message)

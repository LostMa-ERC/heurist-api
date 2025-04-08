class APIException(Exception):
    """Problem calling Heurist API."""


class AuthenticationError(Exception):
    """Error raised when unable to authenticate Heurist login."""

    def __init__(self, message):
        self.message = """Authentication Error.
\tFailed to authenticate Heurist user login.
"""
        super().__init__(self.message)


class MissingParameterException(Exception):
    """Exception raised for a missing parameter."""

    def __init__(self, parameter: str, env_file: str):
        self.message = f"""MissingParameter Exception.
\tMissing parameter '{parameter}'.
\tTried looking in the env file '{env_file}'.
"""
        super().__init__(self.message)


class ReadTimeout(Exception):
    """Exception raised because the data returned by the Heurist \
        server took too long to receive.
    """

    def __init__(self, url: str, timeout: int):
        message = f"""ReadTimeout Error.
\tHeurist's server took too long (> {timeout} seconds) to send data from the following \
URL:
{url}
Solutions:
\t1. Try running the command again and hope the server / your internet is faster.
\t2. Set the READTIMEOUT environment variable and run the command again, in the same \
line, i.e. 'READTIMEOUT=20 heurist' or 'READTIMEOUT=20 python'.
"""
        self.message = message
        super().__init__(self.message)

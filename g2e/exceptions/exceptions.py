"""Application-specific exceptions, useful for normalizing output to the
front-end.
"""


class AppException(Exception):
    """Base exception for serializing all exceptions for JSON.
    """

    def __init__(self, message, original_error, status_code=500):
        super(AppException, self).__init__(message)
        self.message = message
        self.original_error = original_error
        self.status_code = status_code

    @property
    def serialize(self):
        return {
            'error': self.message,
            'original_error': str(self.original_error),
            'error_type': type(self.original_error).__name__
        }


class ParseException(AppException):
    """Exception to be raised when application cannot parse a file.
    """

    def __init__(self, message, original_error, status_code=400):
        super(ParseException, self).__init__(
            message, original_error, status_code
        )


class HttpRequestArgumentsException(AppException):
    """Exception to be raised when an HTTP request arguments are incorrect.
    """

    def __init__(self, message, original_error, status_code=400):
        super(HttpRequestArgumentsException, self).__init__(
            message, original_error, status_code
        )

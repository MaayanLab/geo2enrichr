"""Application-specific exceptions, useful for normalizing output to the
front-end.
"""


class AppException(Exception):
    """Base exception for serializing all exceptions for JSON.
    """

    def __init__(self, message, original_exception, status_code=500):
        super(AppException, self).__init__(message)
        self.message = message
        self.original_exception = original_exception
        self.status_code = status_code

    @property
    def serialize(self):
        return {
            'error': self.message,
            'original_exception': str(self.original_exception)
        }


class ParseException(AppException):
    """Exception to be raised when application cannot parse a file.
    """

    def __init__(self, message, original_exception, status_code=400):
        super(ParseException, self).__init__(message, original_exception, status_code)

"""Application-specific exceptions, useful for normalizing output to the
front-end.
"""


class AppException(Exception):
    """Base exception for serializing all exceptions for JSON.
    """

    def __init__(self, message, python_error=None, status_code=500):
        super(AppException, self).__init__(message)
        self.message = message
        self.python_error = python_error
        self.status_code = status_code

    @property
    def serialize(self):
        result = {
            'error': self.message
        }
        if self.python_error:
            result['python_error'] = str(self.python_error)
            result['error_type'] = type(self.python_error).__name__
        return result


class AuthException(AppException):
    """Exception to be raised when an HTTP request is forbidden.
    """

    def __init__(self, message, python_error=None, status_code=403):
        super(AuthException, self).__init__(message, python_error,
                                            status_code)


class HttpRequestArgumentsException(AppException):
    """Exception to be raised when an HTTP request arguments are incorrect.
    """

    def __init__(self, message, python_error=None, status_code=400):
        super(HttpRequestArgumentsException, self).__init__(message,
                                                            python_error,
                                                            status_code)


class SoftFileParseException(AppException):
    """Exception to be raised when application cannot parse a SOFT file.
    """

    def __init__(self, message, python_error=None, status_code=400):
        super(SoftFileParseException, self).__init__(message, python_error,
                                                     status_code)


class PlatformNotSupportedException(AppException):
    """Exception to be raised when platform is not supported.
    """

    def __init__(self, message, python_error=None, status_code=403):
        super(PlatformNotSupportedException, self).__init__(message,
                                                            python_error,
                                                            status_code)

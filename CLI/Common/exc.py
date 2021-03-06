import sys


class BaseException(Exception):
    """An error occurred."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class CommandError(BaseException):
    """Invalid usage of CLI."""


class InvalidEndpoint(BaseException):
    """The provided endpoint is invalid."""


class CommunicationError(BaseException):
    """Unable to communicate with server."""


class ClientException(Exception):
    """DEPRECATED."""


class HTTPException(ClientException):
    """Base exception for all HTTP-derived exceptions."""
    code = 'N/A'

    def __init__(self, details=None, server_traceback=None):
        self.details = details
        self.server_traceback = server_traceback

    def __str__(self):
        msg = "%s (HTTP %s)" % (self.__class__.__name__,
                                self.code)
        if self.details:
            msg = self.details
        if self.server_traceback:
            msg += "\n%s" % self.server_traceback
        return msg


class HTTPMultipleChoices(HTTPException):
    code = 300

    def __str__(self):
        self.details = ("Requested version of OpenStack Images API is not"
                        "available.")
        return "%s (HTTP %s) %s" % (self.__class__.__name__, self.code,
                                    self.details)


class BadRequest(HTTPException):
    """DEPRECATED."""
    code = 400


class HTTPBadRequest(BadRequest):
    pass


class Unauthorized(HTTPException):
    """DEPRECATED."""
    code = 401


class HTTPUnauthorized(Unauthorized):
    pass


class Forbidden(HTTPException):
    """DEPRECATED."""
    code = 403


class HTTPForbidden(Forbidden):
    pass


class NotFound(HTTPException):
    """DEPRECATED."""
    code = 404


class HTTPNotFound(NotFound):
    pass


class HTTPMethodNotAllowed(HTTPException):
    code = 405


class Conflict(HTTPException):
    """DEPRECATED."""
    code = 409


class HTTPConflict(Conflict):
    pass


class OverLimit(HTTPException):
    """DEPRECATED."""
    code = 413


class HTTPOverLimit(OverLimit):
    pass


class HTTPInternalServerError(HTTPException):
    code = 500


class HTTPNotImplemented(HTTPException):
    code = 501


class HTTPBadGateway(HTTPException):
    code = 502


class ServiceUnavailable(HTTPException):
    """DEPRECATED."""
    code = 503


class HTTPServiceUnavailable(ServiceUnavailable):
    pass


#NOTE(bcwaldon): Build a mapping of HTTP codes to corresponding exception
# classes
_code_map = {}
for obj_name in dir(sys.modules[__name__]):
    if obj_name.startswith('HTTP'):
        obj = getattr(sys.modules[__name__], obj_name)
        _code_map[obj.code] = obj


def from_response(response, message=None, traceback=None):
    """Return an instance of an HTTPException based on httplib response."""
    cls = _code_map.get(response.status, HTTPException)
    return cls(message, traceback)


class NoTokenLookupException(Exception):
    """DEPRECATED."""
    pass


class EndpointNotFound(Exception):
    """DEPRECATED."""
    pass


class InvalidAttribute(ClientException):
    pass
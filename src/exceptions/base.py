from typing import Optional

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):

    STATUS_CODE: Optional[int] = None
    DETAIL: Optional[str] = None

    def __init__(self, **kwargs: dict) -> None:
        if 'extra_msg' in kwargs:
            self.DETAIL = kwargs.pop('extra_msg')

        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
            **kwargs
        )


class InternalServerError(BaseHTTPException):

    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = 'Internal server error'


class BadRequest(BaseHTTPException):

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Bad Request'


class NotAuthenticated(BaseHTTPException):

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Authentication required'


class PermissionDenied(BaseHTTPException):

    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = 'Permission denied'


class NotFound(BaseHTTPException):

    STATUS_CODE = status.HTTP_404_NOT_FOUND

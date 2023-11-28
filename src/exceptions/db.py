from src.exceptions.base import NotFound


class ObjectNotFound(NotFound):

    DETAIL = 'Object not found'

# -*- coding: utf-8 -*-
class APIError(Exception):
    pass


class APIErrorConnection(APIError):
    pass


class APIErrorResponse(APIError):
    pass


class APINetworkError(APIError):
    pass

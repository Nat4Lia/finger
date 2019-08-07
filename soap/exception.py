# -*- coding: utf-8 -*-
class SOAPError(Exception):
    pass


class SOAPErrorConnection(SOAPError):
    pass


class SOAPErrorResponse(SOAPError):
    pass


class SOAPNetworkError(SOAPError):
    pass

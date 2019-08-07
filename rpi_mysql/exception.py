# -*- coding: utf-8 -*-
class DBError(Exception):
    pass


class DBErrorConnection(DBError):
    pass


class DBErrorResponse(DBError):
    pass


# -*- coding: utf-8 -*-
class User(object):
    def __init__(self, user_id, nama, password, privilege, uid):
        self.uid = uid # not really used any more
        self.user_id = user_id
        self.nama = nama
        self.password = password
        self.privilege = privilege

    def __str__(self):
        return '<User>: {} : {}, {} {}, {}'.format(self.uid, self.user_id, self.nama, self.password, self.privilege)

    def __repr__(self):
        return '<User>: {} : {}, {} {}, {}'.format(self.uid, self.user_id, self.nama, self.password, self.privilege)

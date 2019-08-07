# -*- coding: utf-8 -*-
class Attendance(object):
    def __init__(self, user_id, tanggal, jam, status, uid):
        self.uid = uid # not really used any more
        self.user_id = user_id
        self.tanggal = tanggal
        self.status = status
        self.jam = jam

    def __str__(self):
        return '<Attendance>: {} : {}, {} {}, {}'.format(self.uid, self.user_id, self.tanggal, self.jam, self.status)

    def __repr__(self):
        return '<Attendance>: {} : {}, {} {}, {}'.format(self.uid, self.user_id, self.tanggal, self.jam, self.status)

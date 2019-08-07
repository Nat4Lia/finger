# -*- coding: utf-8 -*-
class Template(object):
    def __init__(self, user_id, size, valid, template, tid):
        self.tid = tid # not really used any more
        self.user_id = user_id
        self.size = size
        self.valid = valid
        self.template = template

    def __str__(self):
        return '<Template>: {} : {}, {} {}, {}'.format(self.tid, self.user_id, self.size, self.valid, self.template)

    def __repr__(self):
        return '<Template>: {} : {}, {} {}, {}'.format(self.tid, self.user_id, self.size, self.valid, self.template)

# -*- coding: utf-8 -*-
class Device_Info(object):
    def __init__(self, device_ip, device_name, serial_number, mac, t_users, t_fingers, t_records):
        self.device_ip = device_ip
        self.device_name = device_name
        self.serial_number = serial_number
        self.mac = mac
        self.t_users = t_users
        self.t_fingers = t_fingers
        self.t_records = t_records

    def __str__(self):
        return '<DeviceInfo>: {} : {}, {}, {}, {}, {}, {}'.format(self.device_ip, self.device_name, self.serial_number, self.mac, self.t_users, self.t_fingers, self.t_records)

    def __repr__(self):
        return '<DeviceInfo>: {} : {}, {}, {}, {}, {}, {}'.format(self.device_ip, self.device_name, self.serial_number, self.mac, self.t_users, self.t_fingers, self.t_records)

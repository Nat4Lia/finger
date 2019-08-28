Version = '4.0'
import os, json

from control import Control
from web_api import API
from rpi_mysql import RpiDatabase
from instansi_id import ID_INSTANSI as instansi
from config import DEVICE_IPADDR_LIST

DEVICE_USED = []
DEVICE_FOUND = 0
DEVICE_UNREGISTERED = 0
DEVICE_REGISTERED = 0
DB = None
EABSEN = None

def write_device(device_list) :
    d = []
    device = None
    for data in device_list :
        if data.instansi_id == instansi :
            d.append(data.macaddress)
    try:
        if os.path.exists('device.txt') :
            with open('device.txt', 'r') as f :
                device = json.load(f)
            if device != d :
                with open('device.txt', 'w') as f:
                    json.dump(d, f)
        else :
            with open('device.txt', 'w') as f:
                json.dump(d, f)
    except Exception as e:
        print ('Terminate : {}'.format(e))

def read_device() :
    with open('device.txt','r') as f :
        return json.load(f)

def ping(address, device_mac) :
    from ping import Ping
    from device_status import device_info
    global DEVICE_REGISTERED
    global DEVICE_UNREGISTERED
    global DEVICE_FOUND

    for ip in address :
        print ('check device {}').format(ip)
        p = Ping(ip)
        d = device_info(ip)
        if p.test() :
            DEVICE_FOUND += 1 
            if d.mac in device_mac :
                DEVICE_USED.append(ip)
                DEVICE_REGISTERED += 1
            else :
                DEVICE_UNREGISTERED += 1
try :
    DB = RpiDatabase()
    EABSEN = API()
    write_device(EABSEN.get_reg_mac())
    r_d = read_device()
    ping(DEVICE_IPADDR_LIST, r_d)
    
except Exception as e :
    print ('Terminate {}').format(e.__class__.__name__)

if __name__ == '__main__' :
    print ('{} device found').format(DEVICE_FOUND)
    print ('{} device registered').format(DEVICE_REGISTERED)
    print ('{} device unregistered').format(DEVICE_UNREGISTERED)
    if DEVICE_USED :
        import time
        while True :
            for device in DEVICE_USED :
                command = None
                try:
                    command = EABSEN.get_trigger()
                except Exception as e:
                    print ('get_trigger failed : {}').format(e)
                if command is None : break
                c = Control(device, DB)
                c.status(Version, len(read_device()))
                c.m_admin()
                c.m_users()
                if command.status == 1 :
                    c.m_attendance()
                elif command.status == 2 :
                    pass
                elif command.status == 3 :
                    pass
                elif command.status == 4 :
                    if int(command.instansi_id) == int(instansi) :
                        if DB().is_table_zero('attendance') :
                            DB().truncate('attendance')
                            print ('Clear Successfull')
                        else :
                            print ('Attendance Localhost is Empty')
                elif command.status == 5 :
                    if int(command.instansi_id) == int(instansi) :
                        c.m_attendance(command.patokantanggal)
            
                # c.lanjut()
                print ('delay main_')
                time.sleep(10)

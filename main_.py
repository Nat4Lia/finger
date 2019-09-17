Version = '4.0'
import os, json, time, random, sys

from lcd_i2c import tampil_teks, tampil_gambar, tampil_gauges, tampil_progressbar
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
    # '''Tampilkan Logo'''
    tampil_gambar('logo_prov.png')
    time.sleep(3)
    tampil_gauges(0, 'STARTING...')
    time.sleep(2)
    DB = RpiDatabase()
    tampil_gauges(random.randint(1, 20), 'CHECKING...')
    time.sleep(1)
    EABSEN = API()
    tampil_gauges(random.randint(21, 40), 'CHECKING...')
    time.sleep(1)
    write_device(EABSEN.get_reg_mac())
    tampil_gauges(random.randint(41, 60), 'CHECKING...')
    time.sleep(1)
    r_d = read_device()
    tampil_gauges(random.randint(61, 80), 'CHECKING...')
    time.sleep(1)
    ping(DEVICE_IPADDR_LIST, r_d)
    tampil_gauges(random.randint(81, 99), 'CHECKING...')
    time.sleep(1)
    tampil_gauges(100, 'READY...')
    time.sleep(2)
    
except Exception as e :
    print ('Terminate {}').format(e.__class__.__name__)
    tampil_teks(['ERROR', str(e.__class__.__name__)])
    time.sleep(5)
    tampil_teks(['PROGRAM', 'EXIT'])
    time.sleep(5)
    tampil_teks(['REBOOT TO', 'START AGAIN'])
    time.sleep(5)
    sys.exit()

if __name__ == '__main__' :
    print ('{} device found').format(DEVICE_FOUND)
    print ('{} device registered').format(DEVICE_REGISTERED)
    print ('{} device unregistered').format(DEVICE_UNREGISTERED)
    tampil_teks(['MESIN', 'TERHUBUNG', str(DEVICE_FOUND)])
    time.sleep(3)
    tampil_teks(['MESIN', 'TERDAFTAR', str(DEVICE_REGISTERED)])
    time.sleep(3)
    tampil_teks(['MESIN TIDAK', 'TERDAFTAR', str(DEVICE_UNREGISTERED)])
    time.sleep(3)
    if DEVICE_FOUND == 0 :
        tampil_teks(['TIDAK ADA', 'FINGERPRINT'])
        time.sleep(5)
        tampil_teks(['PROGRAM', 'EXIT'])
        time.sleep(5)
        tampil_teks(['REBOOT TO', 'START AGAIN'])
        time.sleep(5)
        sys.exit()
    
    if DEVICE_USED :
        import time
        while True :
            for device in DEVICE_USED :
                tampil_teks(['CONNECTING', 'TO...', str(device)])
                time.sleep(3)
                command = None
                try:
                    command = EABSEN.get_trigger()[0]
                except Exception as e:
                    print ('get_trigger failed : {}').format(e)
                    tampil_teks(['FAILED GET','COMMAND', 'FROM SERVER'])
                    time.sleep(3)
                if command is None : break
                c = Control(device, DB)
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
                            tampil_teks(['SUCCESS', 'TRUNCATE', 'DATABASE'])
                            time.sleep(3)
                        else :
                            print ('Attendance Localhost is Empty')
                            tampil_teks(['RASPBERRY','DATABASE', 'IS EMPTY'])
                            time.sleep(3)
                elif command.status == 5 :
                    if int(command.instansi_id) == int(instansi) or command.instansi_id is None :
                        c.m_attendance(command.patokantanggal)
                    else :
                        print ('Pengiriman Absensi Ditunda')
                        tampil_teks(['PENGIRIMAN','ABSENSI', 'DITUNDA'])
                        time.sleep(3)
                
                c.status(Version, len(read_device()))
                # c.lanjut()
                print ('delay main_')
                time.sleep(10)

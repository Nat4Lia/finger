# from soap import SOAP
from zk import ZK
from web_api import API
from rpi_mysql import RpiDatabase

db = RpiDatabase()
def tes() :
    # conn = None
    # zk = ZK('192.168.0.90', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try :
        # conn = zk.connect()
        # conn.disable_device()
        # conn.read_sizes()
        # password = 0
        # u = conn.get_users()
        # for user in u :
        #     if user.password :
        #         password += 1
        # data = {
        #         'ip':conn.helper.ip,
        #         'mac':conn.get_mac(),
        #         'sn':conn.get_serialnumber(),
        #         'firmware':conn.get_firmware_version(),
        #         'finger_version':conn.get_fp_version(),
        #         'users':conn.users,
        #         'fingers':conn.fingers,
        #         'passwords':password,
        #         'records':conn.records
        #     }
        # conn.enable_device()
        # db.i_device_info(data)

        # a = API()
        # resp = a.get_reg_mac()
        # # db.truncate('macaddress')                       
        # mac_r = db.get_all_mac()
        # for data in resp :
        #     if data.instansi_id == 19:
        #         if data.macaddress not in mac_r : 
        #             db.insert('macaddress','mac_',data.macaddress)       
        # for data in mac_r :
        #     s = False
        #     for i, x in enumerate(resp) :
        #         if data == x.macaddress : 
        #             s = True
        #             break
        #     if not s :
        #         db.delete_macaddress(data)
    except Exception as e :
        print 'Terminate : {}'.format(e)
# import time
for z in range(0, 1) :
    tes()
    # time.sleep(1)
    # print 'ok'
    
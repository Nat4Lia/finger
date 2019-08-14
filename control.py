from instansi_id import ID_INSTANSI as instansi
from web_api import API
from zk import ZK
from soap import SOAP

class Control(API, ZK, SOAP):
    def __init__ (self, ip_add, db) :
        self.ip_add = ip_add
        self.api = API()
        self.db = db
        self.zk = ZK(ip_add, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        self.soap = SOAP(ip_add)

    def device_info(self) :
        from device_info import Device_Info
        conn = None
        try:
            conn = self.zk.connect()
            conn.disable_device()
            conn.read_sizes()
            device_info = Device_Info(
                self.ip_add, conn.get_device_name(), conn.get_serialnumber(), conn.get_mac(), conn.users, conn.fingers, conn.records
            )
            conn.enable_device()
            return device_info
        except Exception as e:
            print ('Process Terminate : {}'.format(e))
        finally:
            if conn :
                conn.disconnect()



# c = Control('10.10.10.10')
# print c.device_info()
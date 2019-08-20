from instansi_id import ID_INSTANSI as instansi
from web_api import API
from zk import ZK
from soap import SOAP
from token import encrypt



class Control(API, ZK, SOAP):
    def __init__ (self, ip_add, db) :
        self.ip_add = ip_add
        self.api = API()
        self.db = db
        self.zk = ZK(ip_add, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        self.soap = SOAP(ip_add)
        self.device_mac = self.get_dev_mac()
        try:
            self.device_users = []
            for user in self.soap.get_users() :
                self.device_users.append(user.user_id)
        except Exception as e :
            print ('soap.get_users Process Terminate : {}'.format(e.__class__.__name__))

    def get_dev_mac(self) :
        conn = None
        try:
            conn = self.zk.connect()
            conn.disable_device()
            device_mac = conn.get_mac()
            conn.enable_device()
            return device_mac
        except Exception as e:
            print ('get_dev_mac Process Terminate : {}'.format(e))
        finally:
            if conn :
                conn.disconnect()

    # def absensi(self) :
    #     att_sent = self.db.get_all_attendance_sent(self.device_mac)
    #     row_failed = self.db.get_failed_flag(self.device_mac)
    #     if row_failed :
    #         print 'ready'
    #     else:
    #         print 'not ready'

    def m_users(self) : 
        data_queue = {'instansi':instansi, 'macaddress':self.device_mac, 'fingerprint_ip':self.ip_add}
        s_users = None
        try :
            s_users = self.api.get_user_queue(data_queue)
        except Exception as e :
            print ('Cant get user queue : {}'.format(e.__class__.__name__))
        if not s_users :
            return
        import time
        for user in s_users :
            user_auth = None
            auth_type = None
            try :
                user_auth = self.api.get_auth(user.pegawai_id)
                if len(user_auth[0].templatefinger) > 8 :
                    auth_type = 'Fingerprint'
                elif len(user_auth[0].templatefinger) <= 8 :
                    auth_type = 'Password'
            except Exception as e :
                print ('Cant get user auth : {}'.format(e.__class__.__name__))
            if not s_users :
                break
            if user.command == 'daftar' :
                if user.pegawai_id in self.device_users :
                    try :
                        self.api.post_user_queue({
                            'instansi': instansi, 
                            'macaddress': self.device_mac, 
                            'fingerprint_ip': self.ip_add, 
                            'id': user.id, 
                            'token':encrypt("{0}{1}{2}{3}".format(
                                self.device_mac, instansi, self.ip_add, user.id)
                            )
                        })
                    except Exception as e :
                        print ('report queue failed : {}'.format(e.__class__.__name__))
                else :
                    set_status = False
                    try :
                        if auth_type == 'Fingerprint' :
                            print 'regis fp'
                            self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0)
                            for id, auth in enumerate(user_auth) :
                                self.soap.set_user_template(auth.pegawai_id, id, auth.size, auth.valid, auth.templatefinger)
                        elif auth_type == 'Password' :
                            self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0, user_auth[0].templatefinger)
                        set_status = True
                    except Exception as e :
                            print ('set user failed : {}'.format(e.__class__.__name__))
                    finally :
                        if set_status :
                            try :
                                self.api.post_user_queue({
                                    'instansi': instansi, 
                                    'macaddress': self.device_mac, 
                                    'fingerprint_ip': self.ip_add, 
                                    'id': user.id, 
                                    'token':encrypt("{0}{1}{2}{3}".format(
                                        self.device_mac, instansi, self.ip_add, user.id)
                                    )
                                })
                            except Exception as e :
                                print ('report queue failed : {}'.format(e.__class__.__name__))
            print 'delay user'
            time.sleep(15)

    def lanjut(self) :
        print 'fungsi lanjut'
        
        # for user in s_users :
            


# c = Control('10.10.10.10')
# print c.device_info()
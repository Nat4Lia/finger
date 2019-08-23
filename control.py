from instansi_id import ID_INSTANSI as instansi
from web_api import API
from zk import ZK
from soap import SOAP
from token import encrypt

import time

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

        try:
            self.device_admins = []
            for admin in self.soap.get_admins() :
                self.device_admins.append(admin.user_id)
        except Exception as e :
            print ('soap.get_admins Process Terminate : {}'.format(e.__class__.__name__))

        try:
            self.device_attendances = self.soap.get_att()
        except Exception as e :
            print ('soap.get_att Process Terminate : {}'.format(e.__class__.__name__))

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

    def m_users(self) : 
        data_queue = {'instansi':instansi, 'macaddress':self.device_mac, 'fingerprint_ip':self.ip_add}
        s_users = None
        try :
            s_users = self.api.get_user_queue(data_queue)
        except Exception as e :
            print ('Cant get user queue : {}'.format(e.__class__.__name__))
        if not s_users :
            return
        for user in s_users :
            user_auth = None
            auth_type = None
            set_status = False
            # """Penyiapan Data"""
            try :
                user_auth = self.api.get_auth(user.pegawai_id)
                if len(user_auth[0].templatefinger) > 8 :
                    auth_type = 'Fingerprint'
                elif len(user_auth[0].templatefinger) <= 8 :
                    auth_type = 'Password'
            except Exception as e :
                print ('Cant get user auth : {}'.format(e.__class__.__name__))
            
            if user_auth is None :
                break

            # """Command Daftar"""
            if user.command == 'daftar' : 
                if user.pegawai_id in self.device_users :
                    set_status = True
                    pass
                else :
                    try :
                        if auth_type == 'Fingerprint' :
                            print 'regis fp command daftar'
                            self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0)
                            for id, auth in enumerate(user_auth) :
                                self.soap.set_user_template(auth.pegawai_id, id, auth.size, auth.valid, auth.templatefinger)
                        elif auth_type == 'Password' :
                            self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0, user_auth[0].templatefinger)
                        set_status = True
                    except Exception as e :
                        print ('daftar user failed : {}'.format(e.__class__.__name__))
                        
            # """Command Ganti"""
            elif user.command == 'ganti' :
                try:
                    self.soap.delete_user(user.pegawai_id)
                    if auth_type == 'Fingerprint' :
                        print 'regis fp command ganti'
                        self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0)
                        for id, auth in enumerate(user_auth) :
                            self.soap.set_user_template(auth.pegawai_id, id, auth.size, auth.valid, auth.templatefinger)
                    elif auth_type == 'Password' :
                        self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0, user_auth[0].templatefinger)
                    set_status = True
                except Exception as e:
                    print ('ganti user failed : {}'.format(e.__class__.__name__))
            
            # """Command Hapus"""
            elif user.command == 'hapus' :
                set_status = False
                try:
                    self.soap.delete_user(user.pegawai_id)
                    print 'regis fp command hapus'
                    set_status = True
                except Exception as e:
                    print ('hapus user failed : {}'.format(e.__class__.__name__))
            
            # """Lapor Ke Server"""
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
            
    def m_attendance(self) :
        print 'masuk fungsi m_attendance'
        # """Penyiapan Data"""
        # """Jumlah Data Absensi Yang Terkirim"""
        att_sent = self.db.get_all_attendance_sent(self.device_mac)
        if att_sent is None : return
        # """Baris Data Absensi Yang Gagal Terkirim"""
        att_failed = self.db.get_failed_flag(self.device_mac)
        if att_failed is None : return
        # """Baris Data Gagal Disesuaikan Dengan Baris Data Pada Data Asli dan Kemudian Diambil Datanya"""
        collecting_failed = []
        for row_id in att_failed :
            collecting_failed.append(self.device_attendances[row_id[0]])
        # """Mengumpulkan Baris Absensi Yang Baru/Belum Terkirim"""
        collection_new = []
        for row_id in range(att_sent, len(self.device_attendances)) :
            collection_new.append(self.device_attendances[row_id])
        # """Menggabungkan Absensi Yang Gagal dengan Absensi Baru"""
        att_will_send = collecting_failed + collection_new

        # """Iterasi Absensi Yang Dikirim"""
        if att_will_send :
            for att in att_will_send :
                sending = 'Failed'
                try:
                    sending = self.api.post_att({
                        'status':att.status,
                        'instansi':instansi,
                        'jam':att.jam,
                        'tanggal':att.tanggal,
                        'user_id':att.user_id,
                        'macaddress':self.device_mac,
                        'token':encrypt(
                            '{}{}{}{}{}'.format(
                                att.jam,att.tanggal,att.user_id,instansi,att.status
                            )
                        )
                    })
                    print ('Sending status {} : {}'.format(att.uid, sending))
                except Exception as e:
                    print ('Terminate Send : {}, status : {}'.format(e, sending))
                finally :
                    try:
                        self.db.insert_absensi(
                            self.device_mac,
                            att.uid, att.user_id, att.tanggal,
                            att.jam, att.status, sending
                        )
                    except Exception as e:
                        print ('Terminate DB cant insert absensi : {}'.format(e))
        else :
            print ('Semua Absensi Telah Terkirim')
    
    def m_admin(self) :
        s_admin = None
        list_admin = []
        try:
            s_admin = self.api.get_admin()
            for admin in s_admin :
                list_admin.append(int(admin.pegawai_id))
        except Exception as e:
            print ('Cant get admin from server : {}'.format(e.__class__.__name__))
        if s_admin is None : return
        
        print 'server {}'.format(list_admin)
        print 'finger {}'.format(self.device_admins)
        # """Validasi Admin Di Finger"""
        for admin in self.device_admins :
            if int(admin) in list_admin :
                continue
            else :
                try:
                    self.soap.delete_user(admin)
                except Exception as e:
                    print 'Delete Admin Failed : {}'.format(e)

        for admin in s_admin :
            if str(admin.pegawai_id) in self.device_admins : return
            else :
                admin_auth = None
                auth_type = None
                set_status = False
                try:
                    admin_auth = self.api.get_auth(admin.pegawai_id)
                    if len(admin_auth[0].templatefinger) > 8 :
                        auth_type = 'Fingerprint'
                    elif len(admin_auth[0].templatefinger) <= 8 :
                        auth_type = 'Password'
                except Exception as e:
                    print ('Cant get admin auth : {}'.format(e.__class__.__name__))
                
                if admin_auth is None :
                    break
                
                try:
                    print 'mendaftarkan admin'
                    if auth_type == 'Fingerprint' :
                        self.soap.set_user(admin.pegawai_id, admin.nama.replace("'"," "), 14)
                        for id, auth in enumerate(admin_auth) :
                            self.soap.set_user_template(auth.pegawai_id, id, auth.size, auth.valid, auth.templatefinger)
                    elif auth_type == 'Password' :
                        self.soap.set_user(admin.pegawai_id, admin.nama.replace("'"," "), 14, admin_auth[0].templatefinger)
                    set_status = True
                except Exception as e:
                    print ('daftar admin failed : {}'.format(e.__class__.__name__))

                if set_status :
                    print 'daftar admin sukses'

    def lanjut(self) :
        print 'fungsi lanjut'
        # conn = None
        # try:
        #     conn = self.zk.connect()
        #     conn.disable_device()
        #     conn.clear_data()
        #     conn.enable_device()
        # except Exception as e:
        #     print ('clear_data Process Terminate : {}'.format(e))
        # finally:
        #     if conn :
        #         conn.disconnect()
            


# c = Control('10.10.10.10')
# print c.device_info()
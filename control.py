from instansi_id import ID_INSTANSI as instansi
from web_api import API
from zk import ZK
from soap import SOAP
from token import encrypt
from lcd_i2c import tampil_teks, tampil_gambar, tampil_gauges, tampil_progressbar

import time

class Control(API, ZK, SOAP):
    def __init__ (self, ip_add, db) :
        self.ip_add = ip_add
        self.api = API()
        self.db = db
        self.zk = ZK(ip_add, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        self.soap = SOAP(ip_add)
        self.device_mac = self.get_dev_mac()

        self.device_users = []
        try:
            for user in self.soap.get_users() :
                self.device_users.append(user.user_id)
        except Exception as e :
            print ('soap.get_users Process Terminate : {}'.format(e.__class__.__name__))
            
        self.device_admins = []
        try:
            for admin in self.soap.get_admins() :
                self.device_admins.append(admin.user_id)
        except Exception as e :
            print ('soap.get_admins Process Terminate : {}'.format(e.__class__.__name__))

        self.device_attendances = None
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
        # """Validasi User"""
        s_user = None
        list_user = []
        try:
            s_user = self.api.get_user(instansi)
            for user in s_user :
                list_user.append(int(user.pegawai_id))
        except Exception as e:
            print ('Cant get user from server : {}'.format(e.__class__.__name__))
        if s_user is None : pass

        keep_user = 0
        remove_user = 0
        for i, user in enumerate(self.device_users) :
            print ('validating user : {}'.format(user))
            if int(user) in list_user :
                keep_user += 1
                print ('next user')
                continue
            else :
                try:
                    self.soap.delete_user(user)
                    remove_user +=1
                except Exception as e:
                    print ('Delete User Tidak Terdata Failed : {}'.format(e))
        print ('Total User validated : {}\nKeep User : {}\nRemoved User : {}').format(
            len(self.device_users), keep_user, remove_user)

        data_queue = {'instansi':instansi, 'macaddress':self.device_mac, 'fingerprint_ip':self.ip_add}
        s_users = None
        try :
            s_users = self.api.get_user_queue(data_queue)
        except Exception as e :
            print ('Cant get user queue : {}'.format(e.__class__.__name__))
            tampil_teks(['SERVER', 'CONNECTION', 'ERROR'])
            time.sleep(3)
            tampil_teks(['CANT GET', 'USER QUEUE', 'FROM SERVER'])
            time.sleep(3)
        if not s_users :
            return
        tampil_teks(['MANAGE USERS'])
        time.sleep(3)
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
                tampil_teks(['SERVER', 'CONNECTION', 'ERROR'])
                time.sleep(3)
                tampil_teks(['CANT GET', 'USER AUTH', 'FROM SERVER'])
                time.sleep(3)
            
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
                            print ('regis fp command daftar')
                            self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0)
                            for id, auth in enumerate(user_auth) :
                                self.soap.set_user_template(auth.pegawai_id, id, auth.size, auth.valid, auth.templatefinger)
                        elif auth_type == 'Password' :
                            self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0, user_auth[0].templatefinger)
                        set_status = True
                        tampil_teks(['MENDAFTARKAN', user.nama, auth_type])
                        time.sleep(3)
                    except Exception as e :
                        print ('daftar user failed : {}'.format(e.__class__.__name__))
                        
            # """Command Ganti"""
            elif user.command == 'ganti' :
                try:
                    self.soap.delete_user(user.pegawai_id)
                    if auth_type == 'Fingerprint' :
                        print ('regis fp command ganti')
                        self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0)
                        for id, auth in enumerate(user_auth) :
                            self.soap.set_user_template(auth.pegawai_id, id, auth.size, auth.valid, auth.templatefinger)
                    elif auth_type == 'Password' :
                        self.soap.set_user(user.pegawai_id, user.nama.replace("'"," "), 0, user_auth[0].templatefinger)
                    set_status = True
                    tampil_teks(['GANTI', auth_type, user.nama])
                    time.sleep(3)
                except Exception as e:
                    print ('ganti user failed : {}'.format(e.__class__.__name__))
            
            # """Command Hapus"""
            elif user.command == 'hapus' :
                set_status = False
                try:
                    self.soap.delete_user(user.pegawai_id)
                    print ('regis fp command hapus')
                    set_status = True
                    tampil_teks(['HAPUS USER', user.nama])
                    time.sleep(3)
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
            
    def m_attendance(self, tanggal=None) :
        print('m_attendance')
        tampil_teks(['PENGIRIMAN','ABSENSI'])
        time.sleep(3)
        while True :

            if self.device_attendances is None : return
            att_will_send = []
            if tanggal is not None :
                print ('masuk fungsi m_attendance by tanggal')
                from datetime import datetime
                attendance_new = []
                s_date = datetime.strptime(tanggal, '%d-%m-%Y')
                for att in self.device_attendances :
                    if datetime.strptime(att.tanggal, '%d-%m-%Y') >= s_date :
                        attendance_new.append(att)
                att_will_send = attendance_new
            else :
                print ('masuk fungsi m_attendance')
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
                for i, att in enumerate(att_will_send) :
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
                        import datetime
                        tampil_progressbar(len(att_will_send), i+1, 'PENGIRIMAN ABSEN', str(att.tanggal.strftime("%d %b %Y")), str(sending))
                        time.sleep(2)
                        try:
                            self.db.insert_absensi(
                                self.device_mac,
                                att.uid, att.user_id, att.tanggal,
                                att.jam, att.status, sending
                            )
                            print('Sending {}/{}/{}/{}/{}').format(
                                att.uid, att.user_id, att.tanggal,
                                att.jam, att.status
                            )
                        except Exception as e:
                            print ('Terminate DB cant insert absensi : {}'.format(e))
            
            print('delay absensi for test only')
            time.sleep(15)
            
            new_device_attendances = None
            try:
                new_device_attendances = self.soap.get_att()
            except Exception as e :
                print ('soap.get_att Process Terminate : {}'.format(e.__class__.__name__))
            finally :
                if new_device_attendances is None : return
                if len(new_device_attendances) > len(self.device_attendances) :
                    self.device_attendances = new_device_attendances
                else :
                    if len(self.device_attendances) >= 50000 :
                        conn = None
                        try:
                            conn = self.zk.connect()
                            conn.disable_device()
                            conn.clear_attendance()
                            conn.enable_device()
                            self.db.delete_by_mac(self.device_mac)
                        except Exception as e:
                            print ('clear_attendance Process Terminate : {}'.format(e))
                        finally:
                            if conn :
                                conn.disconnect()
                    return

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
        
        print ('server {}'.format(list_admin))
        print ('finger {}'.format(self.device_admins))

        # """Validasi Duplikat Admin Di Device, jika duplicate, semua admin dihapus"""
        if len(set(self.device_admins)) != len(self.device_admins):
            for admin in self.device_admins :
                try:
                    self.soap.delete_user(admin)
                except Exception as e:
                    print ('Delete Duplikat Admin Failed : {}').format(e)
            self.device_admins = []

        # """Validasi Admin Di Finger"""
        for admin in self.device_admins :
            if int(admin) in list_admin :
                continue
            else :
                try:
                    self.soap.delete_user(admin)
                except Exception as e:
                    print ('Delete Admin Tidak Terdata Failed : {}').format(e)

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
                    print ('mendaftarkan admin')
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
                    print ('daftar admin sukses')

    def status(self, version, countmac) :
        send_status = 'Disconnected'
        precentabsen = 0
        try:
            self.api.post_rpi_status({
                'ip' : self.ip_add,
                'versi' :  version,
                'jumlahmac' : countmac,
                'jumlahpegawaifinger' : len(self.device_users),
                'jumlahadminfinger' : len(self.device_admins),
                'jumlahabsensifinger' : len(self.device_attendances),
                'jumlahpegawailocal' : len(self.device_users),
                'jumlahadminlocal' : len(self.device_admins),
                'jumlahabsensilocal' : self.db.get_success_flag(self.device_mac),
                'instansi_id' : instansi,
                'token' : encrypt(
                    '{}{}{}{}{}{}{}{}{}{}'.format(
                        self.ip_add, version,
                        countmac, len(self.device_users), 
                        len(self.device_admins), len(self.device_attendances),
                        len(self.device_users), len(self.device_admins),
                        self.db.get_success_flag(self.device_mac), instansi
                    )
                )
            })
            try : 
                percentabsen = float(len(self.device_attendances)) / float(self.db.get_success_flag(self.device_mac)) * 100
            except ZeroDivisionError :
                percentabsen = 0
            tampil_teks(['VERSI : '+str(version), 'PEGAWAI : '+str(len(self.device_users)), 'ABSENSI : '+str(int(percentabsen))+'%', 'CONNECTED'])
            time.sleep(3)
        except Exception as e:
            tampil_teks(['VERSI : '+str(version), 'PEGAWAI : '+str(len(self.device_users)), 'ABSENSI : '+str(int(percentabsen))+'%', 'DISCONNECTED'])
            time.sleep(3)
            print ('Send status failed : {}').format(e) 

    # def lanjut(self) :
    #     print ('fungsi lanjut')
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
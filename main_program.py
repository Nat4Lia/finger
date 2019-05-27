from mesin import Mesin
from rpidatabase import RpiDatabase
import os
from api import API
from config import server_api_param as api
from subprocess import check_call as run
import time
from config import skpd
import json
import lcd_

#logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# create a file handler
handler = logging.FileHandler('Error.log')
handler.setLevel(logging.ERROR)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
#

# update program
def update(version):
    SRC = '/home/pi/finger'
    CMD = {
            'REMOVESOURCE'  : 'sudo rm -rf %s',
            'CLONETOSOURCE' : 'sudo git clone https://github.com/Nat4Lia/finger.git %s',
            'COPYTOETC'     : 'sudo cp -R /home/pi/finger /etc/',
            'REBOOT'        : 'sudo reboot'
    }

    lcd_.teks(text1='UPDATE PROGRAM', text2='RASPBERRY')
    time.sleep(1.2)
    if os.path.isdir(SRC) :
        run(CMD['REMOVESOURCE'] % SRC,shell=True)
        run(CMD['CLONETOSOURCE'] % SRC,shell=True)
        run(CMD['COPYTOETC'], shell=True)
        RpiDatabase().update_version(version)
    else :
        run(CMD['CLONETOSOURCE'] % SRC,shell=True)
        run(CMD['COPYTOETC'], shell=True)
        from config import version_table
        RpiDatabase().insert(
            version_table['table']['name'],
            version_table['table']['column'][0]['name'],
            version
        )
    lcd_.teks(text1='PROGRAM RASPBERRY', text2='UPDATE', text3='KE VERSI %s' % RpiDatabase().get_version())
    time.sleep(1.2)
    time.sleep(5)
    lcd_.teks(text1='RASPBERRY', text2='AKAN MELAKUKAN', text3='RESTART')
    time.sleep(1.2)
    run(CMD['REBOOT'], shell=True)
#

# check_connection
def check_connection(address) :
    response = os.system("ping -c 3 " + address)
    if response == 0:
        return True
    else:
        return False
#

# otp
def encrypt(data):
    key = 'D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121'
    textASCII = [ord(x) for x in data]
    keyASCII = [ord(x) for x in key]
    encASCII = [(41+((x+y)%26)) for x, y in zip (textASCII, keyASCII)]
    encText = ''.join(chr(x) for x in encASCII)
    return encText
#

# save_macaddress
def save_macaddress() :
    mac_local   = RpiDatabase().get_all_mac()
    mac_server  = API().get_server(api['Macaddress'])
    lcd_.teks(text1='MENGAMBIL',text2='DATA',text3='MACADDRESS')
    time.sleep(1.2)
    if mac_server is 'ServerConnectionError' or mac_server is None :
        #tampilkan bahwa koneksi error
        lcd_.teks(text1='GAGAL',text2='MENGAMBIL',text3='DATA MACADDRESS')
        time.sleep(1.2)
    else :
        for progress, mac_server_ in enumerate(mac_server) :
            lcd_.progress_bar(progress+1, len(mac_server), text="CHECKING MAC")
            lcd_.disp.image(lcd_.image)
            lcd_.disp.display()
            #check_macaddress_exists
            if RpiDatabase().is_macaddress_registered(mac_server_['macaddress']) :
                # print 'mac terdaftar'
                continue
            else :
                # print 'mendaftarkan'+mac_server_['macaddress']
                RpiDatabase().insert('macaddress', 'mac_', mac_server_['macaddress'])
#

# laporan managenment employee
def lapor_employee(mac_address, ip_address, queue_id, skpd=skpd) :
    token_lapor = encrypt(
        "{0}{1}{2}{3}".format(
            mac_address,
            skpd,
            ip_address,
            queue_id
        )
    )
    lapor = API().post_server(
        api['PostQueue'],
        {
            'instansi'          : skpd,
            'macaddress'        : mac_address,
            'fingerprint_ip'    : ip_address,
            'id'                : queue_id,
            'token'             : token_lapor
        }
    )
    return lapor
#

# menghapus semua isi tabel attendance
def clear_all_attendance () :
    RpiDatabase().truncate('attendance')
#
      
# menghapus semua tabel attendance berdasarkan mac
def clear_attendance_by_mac (_macaddress) :
    RpiDatabase().delete_by_mac(_macaddress) 
#          

#inisialisasi awal program start

def tesdata(namafile) :
    with open('{}'.format(namafile), 'r') as tesdata :
        file_json = json.load(tesdata)
        return file_json

class MainProgram(RpiDatabase, API, Mesin) :

    def __init__(self, ip_addr) :
        API.__init__(self)
        RpiDatabase.__init__(self)
        Mesin.__init__(self, ip_addr)
        self.is_mesin_registered = self.is_macaddress_registered(self.mac_address)
        self.count_attendance_sent = self.get_all_attendace_sent(self.mac_address)

#Pengiriman Absen        
    def send_attendance(self) :
        if self.is_mesin_registered : #Jika Mesin Terdaftar
        #ambil jumlah absensi yg terkirim
            attendance_sent = self.get_all_attendace_sent(self.mac_address)
        #

        #ambil row failed
            get_row_local_att_failed = self.get_failed_flag(self.mac_address)
        #
        
        #jika datanya ada
            if ((get_row_local_att_failed is not None) 
                and 
                (attendance_sent is not None)
                and
                (self.attendance is not None)) :

            #mengumpulkan data absensi yg failed dari mesin sesuai dengan data local
                attendance_failed = []
                for row_id in get_row_local_att_failed :
                    attendance_failed.append(self.attendance[row_id[0]])
            #

            #mengumupulkan absensi belum terkirim
                attendance_new = []
                for row_id in range(attendance_sent, len(self.attendance)) :
                    attendance_new.append(self.attendance[row_id])
            #

            #absensi yang akan dikirim (gabungan absensi failed dan absensi belum terkirim)
                attendance_will_send = attendance_failed + attendance_new
            #

            # iterasi absensi yang akan dikirim
                lcd_.teks(text1='BERSIAP', text2='MENGIRIMKAN', text3='ABSENSI')
                time.sleep(1.2)

                if attendance_will_send :
                    try :
                        for progress, attendance in enumerate(attendance_will_send) :#Kasih loading pengiriman

                        # buat otp
                            token = encrypt(
                                attendance['Jam'] +
                                attendance['Tanggal'] +
                                attendance['PIN'] +
                                str(skpd) +
                                attendance['Status']
                            )
                        #

                        # kirimkan absensi
                            _send_attendance = self.post_server(
                                api['Absensi'], {
                                    'status'    : attendance['Status'], 
                                    'instansi'  : skpd, 
                                    'jam'       : attendance['Jam'], 
                                    'tanggal'   : attendance['Tanggal'], 
                                    'user_id'   : attendance['PIN'],
                                    'macaddress': self.mac_address,
                                    'token'     : token
                                }
                            )
                        #
                            lcd_.progress_bar(progress+1, len(attendance_will_send), text=attendance['Tanggal'])
                            lcd_.disp.image(lcd_.image)
                            lcd_.disp.display()

                        # jika pengiriman diterima, insert ke database
                            if _send_attendance is 'Success' or _send_attendance is 'Failed' :
                                self.insert_absensi(
                                    self.mac_address,
                                    attendance['Row_ID'],
                                    attendance['PIN'],
                                    attendance['Tanggal'],
                                    attendance['Jam'],
                                    attendance['Status'],
                                    _send_attendance
                                )
                            else :
                                lcd_.teks(text1='KONEKSI', text2='SERVER', text3='BERMASALAH')
                                time.sleep(1.2) 
                                lcd_.teks(text1='TIDAK DAPAT', text2='MENGIRIM ABSENSI', text3='KE SERVER')
                                time.sleep(1.2)
                                raise Exception
                                # print 'KONEKSI KE SERVER BERMASALAH'
                                # print 'TIDAK DAPAT MENGIRIM ABSENSI KE SERVER'
                            time.sleep(1.2)
                        #
                    except Exception as error :
                        lcd_.teks(text2=str(error))
                        time.sleep(1.2)
                        lcd_.teks(text1='GAGAL', text2='MENGIRIMKAN', text3='ABSENSI')
                        time.sleep(1.2)
                else :
                    lcd_.teks(text1='TIDAK ADA', text2='ABSENSI', text3='BARU')
                    time.sleep(1.2)
        #
            else :
                lcd_.teks(text1='KESALAHAN PADA', text2='DATABASE', text3='RASPBERRY')
                time.sleep(1.2)
                lcd_.teks(text1='HARAP', text2='RESTART', text3='RASPBERRY')
                time.sleep(1.2)
                lcd_.teks(text1='JIKA PESAN INI', text2='SELALU MUNCUL')
                time.sleep(1.2)
                lcd_.teks(text1='SEGERA', text2='HUBUNGI', text3='DISKOMINFO')
                time.sleep(1.2)
                # print 'KESALAHAN PADA DATABASE RASPBERRY'
                # print 'HARAP RESTART RASPBERRY'
                # print 'JIKA PESAN INI SELALU MUNCUL, SEGERA HUBUNGI DISKOMINFO'
            
        else :
            lcd_.teks(text1='PERIKSA APAKAH', text2='MESIN TERDAFTAR', text3='DI DISKOMINFO')
            time.sleep(1.2)
            lcd_.teks(text1='PERIKSA KEMBALI', text2='KONEKSI MESIN', text3='DENGAN RASPBERRY')
            time.sleep(1.2)
            # print 'PERIKSA APAKAH MESIN SUDAH TERDAFTAR DI DISKOMINFO'
            # print 'PERIKSA KEMBALI KONEKSI MESIN DENGAN RASPBERRY'
#

#Manajemen User
    def management_employee (self) :
        print 'management employee'
        api_pegawai         = self.post_return_data(
                                                        api['GetQueue'],
                                                        {
                                                            'instansi'      : skpd,
                                                            'macaddress'    : self.mac_address,
                                                            'fingerprint_ip': self.ip_addr
                                                        }
                                    )
        try :
            if api_pegawai is 'ServerConnectionError' :
                raise Exception 
            else :
                if self.user is None :
                    raise Exception
                else :
                    for data in api_pegawai :
                    #mendaftarkan pegawai
                        cek = self.check_user(data['pegawai_id']) #cek pendaftaran
                        # print 'CEK '+data['nama']
                        api_sidikjari = self.get_server(api['Autentikasi'] % data['pegawai_id']) #ambil sidik jari
                        # print len(api_sidikjari)
                        if str(data['command']) == 'daftar' :
                        #cek user terdaftar/tidak
                            if cek is True :
                            #sudah terdaftar
                                laporan = lapor_employee(
                                    self.mac_address,
                                    self.ip_addr,
                                    data['id']
                                )
                                lcd_.teks(text1=data['nama'], text2='TERDAFTAR')
                                time.sleep(1.2)
                                # print 'LAPORAN '+laporan
                                # print 'SUDAH TERDAFTAR'
                            #    
                            elif cek is False :
                            #belum terdaftar
                            #mengambil data api sidik jari
                                if api_sidikjari is 'ServerConnectionError' :
                                    raise Exception
                                else :
                                #password
                                    if len(api_sidikjari[0]['templatefinger']) <= 8 :
                                    #daftarkan pegawai
                                        set_pegawai = self.set_user(
                                            data['pegawai_id'],
                                            data['nama'].replace("'", " "),
                                            api_sidikjari[0]['templatefinger']
                                        )
                                        if set_pegawai is True:
                                            laporan = lapor_employee(
                                                self.mac_address,
                                                self.ip_addr,
                                                data['id']
                                            )
                                            lcd_.teks(text1=data['nama'], text2='TERDAFTAR')
                                            time.sleep(1.2)
                                            # print 'LAPORAN '+laporan
                                            # print 'SUKSES USER PASSWORD'
                                        elif set_pegawai is False :
                                            lcd_.teks(text1=data['nama'], text2='GAGAL', text3='TERDAFTAR')
                                            time.sleep(1.2)
                                        elif set_pegawai is None :
                                            raise Exception
                                    #
                                #
                                #sidik jari
                                    elif len(api_sidikjari[0]['templatefinger']) > 8 :
                                    #daftarkan pegawai
                                        set_pegawai = self.set_user(
                                            data['pegawai_id'],
                                            data['nama'].replace("'", " "),
                                            None
                                        )
                                        if set_pegawai is True:
                                        #daftarkan sidik jari
                                            # print 'SUKSES USER'
                                            set_sidikjari = self.set_template(api_sidikjari)
                                            if set_sidikjari is True:
                                                laporan = lapor_employee(
                                                    self.mac_address,
                                                    self.ip_addr,
                                                    data['id']
                                                )
                                                lcd_.teks(text1=data['nama'], text2='TERDAFTAR')
                                                time.sleep(1.2)
                                                # print 'LAPORAN '+laporan
                                                # print 'SUKSES SIDIK JARI'
                                            elif set_sidikjari is False :
                                                lcd_.teks(text1=data['nama'], text2='GAGAL', text3='TERDAFTAR')
                                                time.sleep(1.2)
                                                print 'GAGAL SIDIK JARI'
                                            elif set_sidikjari is None :
                                                raise Exception
                                        #
                                        elif set_pegawai is False :
                                            lcd_.teks(text1='GAGAL', text2='MENDAFTARKAN', text3=data['nama'])
                                            time.sleep(1.2)
                                            # print 'GAGAL USER'
                                        elif set_pegawai is None :
                                            raise Exception
                                    #
                            #        
                            #
                            elif cek is None :
                                raise Exception
                        #
                    #
                        elif str(data['command']) == 'ganti' :
                        #cek user terdaftar/tidak
                            if cek is True :
                                if api_sidikjari is 'ServerConnectionError' :
                                    raise Exception
                                else :
                                #password
                                    if len(api_sidikjari[0]['templatefinger']) <= 8 :
                                    #hapus user, ganti dengan password
                                        del_user = self.delete_user(data['pegawai_id'])
                                        if del_user :
                                            set_pegawai = self.set_user(
                                                data['pegawai_id'],
                                                data['nama'].replace("'", " "),
                                                api_sidikjari[0]['templatefinger']
                                            )
                                            if set_pegawai is True :
                                                laporan = lapor_employee(
                                                    self.mac_address,
                                                    self.ip_addr,
                                                    data['id']
                                                )
                                                # print 'LAPORAN '+laporan
                                                # print 'SUKSES GANTI KE PASSWORD'
                                                lcd_.teks(text1=data['nama'], text2='GANTI KE', text3='PASSWORD')
                                                time.sleep(1.2)
                                                
                                            elif set_pegawai is False :
                                                lcd_.teks(text1=data['nama'], text2='GAGAL GANTI KE', text3='PASSWORD')
                                                time.sleep(1.2)
                                                # print 'GAGAL GANTI KE PASSWORD'
                                            elif set_pegawai is None :
                                                raise Exception
                                        else :
                                            raise Exception
                                    #
                                #
                                #sidik jari
                                    elif len(api_sidikjari[0]['templatefinger']) > 8 :
                                    #hapus user, ganti dengan password
                                        del_user = self.delete_user(data['pegawai_id'])
                                        if del_user :
                                        #daftarkan pegawai
                                            set_pegawai = self.set_user(
                                                data['pegawai_id'],
                                                data['nama'].replace("'", " "),
                                                None
                                            )
                                            if set_pegawai is True:
                                            #daftarkan sidik jari
                                                # print 'SUKSES USER'
                                                set_sidikjari = self.set_template(api_sidikjari)
                                                if set_sidikjari is True:
                                                    laporan = lapor_employee(
                                                        self.mac_address,
                                                        self.ip_addr,
                                                        data['id']
                                                    )
                                                    # print 'LAPORAN '+laporan
                                                    # print 'SUKSES MENGGANTI JARI'
                                                    lcd_.teks(text1=data['nama'], text2='GANTI KE', text3='SIDIK JARI')
                                                    time.sleep(1.2)
                                                elif set_sidikjari is False :
                                                    lcd_.teks(text1=data['nama'], text2='GAGAL GANTI KE', text3='SIDIK JARI')
                                                    time.sleep(1.2)
                                                elif set_sidikjari is None :
                                                    raise Exception
                                            #
                                            elif set_pegawai is False :
                                                # print 'GAGAL MENGGANTI SIDIK JARI USER'
                                                lcd_.teks(text1='GAGAL', text2='GANTI AUTENTIKASI', text3=data['nama'])
                                                time.sleep(1.2)
                                            elif set_pegawai is None :
                                                raise Exception
                                        #
                                        else :
                                            raise Exception
                                    #
                                #
                            elif cek is False :
                                lcd_.teks(text1=data['nama'], text2='TIDAK TERDAFTAR', text3='DI MESIN')
                                time.sleep(1.2)
                            elif cek is None :
                                raise Exception
                        #
                        elif str(data['command']) == 'hapus' :
                        # cek user terdaftar/tidak
                            if cek is True :
                                #hapus user
                                    del_user = self.delete_user(data['pegawai_id'])
                                    if del_user :
                                        laporan = lapor_employee(
                                            self.mac_address,
                                            self.ip_addr,
                                            data['id']
                                        )
                                        lcd_.teks(text1=data['nama'], text2='TERHAPUS DARI', text3='MESIN')
                                        time.sleep(1.2)
                                        # print 'LAPORAN '+laporan
                                        # print 'SUKSES MENGHAPUS PEGAWAI'
                                    else :
                                        raise Exception
                                #
                            elif cek is False :
                                lcd_.teks(text1=data['nama'], text2='TIDAK TERDAFTAR', text3='DI MESIN')
                                time.sleep(1.2)
                                laporan = lapor_employee(
                                                        self.mac_address,
                                                        self.ip_addr,
                                                        data['id']
                                                    )
                            elif cek is None :
                                raise Exception
                        #
        except Exception as error :
            logger.error(error)
            lcd_.teks(text1='TERJADI KESALAHAN', text2='MANAGEMENT', text3='EMPLOYEE')
            time.sleep(1.2)
            # print 'error'+str(error)
#        

#Pengiriman Status
    def status_data(self) :
        try :
            token = encrypt(
                str(self.ip_addr) +
                str(self.get_version()) +
                str(self.count_mac) +
                str(len(self.user)) +
                str(len(self.admin)) +
                str(len(self.attendance)) +
                str(len(self.user)) +
                str(len(self.admin)) +
                str(self.get_success_flag(self.mac_address)) +
                str(skpd)
            )

            _send_status = self.post_server(
                api['Status'], {
                    'ip'                    : self.ip_addr,
                    'versi'                 : self.get_version(),
                    'jumlahmac'             : self.count_mac,
                    'jumlahpegawaifinger'   : len(self.user),
                    'jumlahadminfinger'     : len(self.admin),
                    'jumlahabsensifinger'   : len(self.attendance),
                    'jumlahpegawailocal'    : len(self.user),
                    'jumlahadminlocal'      : len(self.admin),
                    'jumlahabsensilocal'    : self.get_success_flag(self.mac_address),
                    'instansi_id'           : skpd,
                    'token'                 : token
                    
                }
            )
            if _send_status is 'Success' or _send_status is 'Failed' :
                tulisan = 'CONNECTED'
            else :
                tulisan = 'DISCONNECTED'
            lcd_.teks(text1='VERSI : %s' % self.get_version(), 
                    text2='JUMLAH PEGAWAI : %s' % len(self.user), 
                    text3='STATUS : %s' % tulisan)
            
        except TypeError as error :
            logger.error(error)
            # print 'Koneksi Fingerprint Error'
#

#Manajemen Admin
    def management_admin(self) :
        api_admin         = self.get_server(api['Admin'])
        try :
            if api_admin is 'ServerConnectionError' :
                raise Exception 
            else :
                if self.admin is None :
                    raise Exception
                else :
                    for data in api_admin :
                        cek = self.check_user(data['pegawai_id'])
                        api_sidikjari = self.get_server(api['Autentikasi'] % data['pegawai_id'])
                        if cek is True :
                            continue
                        elif cek is False :
                            if api_sidikjari is 'ServerConnectionError' :
                                raise Exception
                            else :
                                if len(api_sidikjari[0]['templatefinger']) <= 8 :
                                    set_admin = self.set_admin(
                                        data['pegawai_id'],
                                        data['nama'].replace("'", " "),
                                        api_sidikjari[0]['templatefinger']
                                    )
                                    if set_admin is False :
                                        continue
                                    elif set_admin is None :
                                        raise Exception
                                elif len(api_sidikjari[0]['templatefinger']) > 8 :
                                    set_admin = self.set_admin(
                                        data['pegawai_id'],
                                        data['nama'].replace("'", " "),
                                        None
                                    )
                                    if set_admin is True:
                                        set_sidikjari = self.set_template(api_sidikjari)
                                        if set_sidikjari is False :
                                            continue
                                        elif set_sidikjari is None :
                                            raise Exception
                                    elif set_admin is False :
                                        continue
                                    elif set_admin is None :
                                        raise Exception
                        elif cek is None :
                            raise Exception
        except Exception as error:
            logger.error(error)
            # print error
            # lcd_.teks(text1='TERJADI KESALAHAN', text2='MANAGEMENT', text3='ADMIN')
            # time.sleep(1.2)
#

#clear data 50000
    def clear_absensi(self) :
        # print self.count_attendance_sent
        # print len(self.attendance)

        if len(self.attendance) >= 50000 and self.count_attendance_sent >= 50000 :
            print 'hapus'
            self.clear_attendance()
            RpiDatabase().truncate('attendance')
            lcd_.teks(text1='MENGHAPUS', text2='DATA', text3='ATTENDANCE')
            time.sleep(1.2)
            run('sudo reboot', shell=True)
        else :
            pass
            

# validasi user
    def validasi_user(self) :
        try :
            data_API    = self.get_server(api['Pegawai'])
            data_Mesin  = self.user
            if data_API is 'ServerConnectionError' :
                # print 'ada error'
                raise Exception
            else :
                if data_Mesin is None :
                    raise Exception
                else :
                    if len(data_API) == len(data_Mesin) :
                        lcd_.teks(text1='USER', text2='TELAH', text3='TERVALIDASI')
                        time.sleep(1.2)
                    else :
                        lcd_.teks(text1='VALIDASI', text2='USER')
                        time.sleep(1.2)
                        for progress, user_mesin in enumerate(data_Mesin) :
                            hasil = False
                            lcd_.progress_bar(progress+1, len(data_Mesin), text=user_mesin['Nama'])
                            lcd_.disp.image(lcd_.image)
                            lcd_.disp.display()
                            for user_API in data_API:
                                if str(user_mesin['PIN']) == str(user_API['pegawai_id']) :
                                    hasil = True
                                    break
                                else :
                                    continue
                            if not hasil :
                                self.delete_user(user_mesin['PIN'])
        except Exception as error :
            logger.error(error)
            # print error   
#

#Pengiriman Absen Khusus     
    def spesific_send_attendance(self, tanggal) :
        from datetime import datetime
        if self.is_mesin_registered : #Jika Mesin Terdaftar
        #ambil jumlah absensi yg terkirim
            attendance_sent = self.get_all_attendace_sent(self.mac_address)
        #

        #ambil row failed
        #    get_row_local_att_failed = self.get_failed_flag(self.mac_address)
        #
        
        #jika data attendance dari fingerprint ada
            if self.attendance is not None :

            #mengumpulkan data absensi yg failed dari mesin sesuai dengan data local
            #    attendance_failed = []
            #    for row_id in get_row_local_att_failed :
            #        attendance_failed.append(self.attendance[row_id[0]])
            #

            #mengumpulkan absensi diatas tanggal yg ditentukan
                attendance_new = []
                attendance_old = []
                for row_id in range(attendance_sent, len(self.attendance)) :
                    tgl_khusus = datetime.strptime(tanggal, '%Y-%m-%d')
                    tgl_fingerprint = datetime.strptime(self.attendance[row_id]['Tanggal'], '%Y-%m-%d') #convert str to date
                    if tgl_fingerprint >= tgl_khusus :#jika data absensi diatas tanggal yg ditentukan
                        attendance_new.append(self.attendance[row_id])#dikumpulkan menjadi absensi baru
                    else :                         #jika tidak
                        attendance_old.append(self.attendance[row_id])#dikumpulkan menjadi absensi lama
            #

            #simpan absensi lama dengan status success
                for attendance in attendance_old :
                    self.insert_absensi(
                        self.mac_address,
                        attendance['Row_ID'],
                        attendance['PIN'],
                        attendance['Tanggal'],
                        attendance['Jam'],
                        attendance['Status'],
                        'Success'
                    )
            #

            #absensi yang akan dikirim (gabungan absensi failed dan absensi belum terkirim)
                #attendance_will_send = attendance_failed + attendance_new
            #

            # iterasi absensi yang akan dikirim
                lcd_.teks(text1='BERSIAP', text2='MENGIRIMKAN', text3='ABSENSI')
                time.sleep(1.2)

                if attendance_new :
                    try :
                        for progress, attendance in enumerate(attendance_new) :#Kasih loading pengiriman

                        # buat otp
                            token = encrypt(
                                attendance['Jam'] +
                                attendance['Tanggal'] +
                                attendance['PIN'] +
                                str(skpd) +
                                attendance['Status']
                            )
                        #

                        # kirimkan absensi
                            _send_attendance = self.post_server(
                                api['Absensi'], {
                                    'status'    : attendance['Status'], 
                                    'instansi'  : skpd, 
                                    'jam'       : attendance['Jam'], 
                                    'tanggal'   : attendance['Tanggal'], 
                                    'user_id'   : attendance['PIN'],
                                    'macaddress': self.mac_address,
                                    'token'     : token
                                }
                            )
                        #
                            lcd_.progress_bar(progress+1, len(attendance_new), text=attendance['Tanggal'])
                            lcd_.disp.image(lcd_.image)
                            lcd_.disp.display()

                        # jika pengiriman diterima, insert ke database
                            if _send_attendance is 'Success' or _send_attendance is 'Failed' :
                                self.insert_absensi(
                                    self.mac_address,
                                    attendance['Row_ID'],
                                    attendance['PIN'],
                                    attendance['Tanggal'],
                                    attendance['Jam'],
                                    attendance['Status'],
                                    _send_attendance
                                )
                            else :
                                lcd_.teks(text1='KONEKSI', text2='SERVER', text3='BERMASALAH')
                                time.sleep(1.2) 
                                lcd_.teks(text1='TIDAK DAPAT', text2='MENGIRIM ABSENSI', text3='KE SERVER')
                                time.sleep(1.2)
                                raise Exception
                                # print 'KONEKSI KE SERVER BERMASALAH'
                                # print 'TIDAK DAPAT MENGIRIM ABSENSI KE SERVER'
                            time.sleep(1.2)
                        #
                    except Exception as error :
                        lcd_.teks(text2=str(error))
                        time.sleep(1.2)
                        lcd_.teks(text1='GAGAL', text2='MENGIRIMKAN', text3='ABSENSI')
                        time.sleep(1.2)
                else :
                    lcd_.teks(text1='TIDAK ADA', text2='ABSENSI', text3='BARU')
                    time.sleep(1.2)
        #
            else :
                lcd_.teks(text1='KESALAHAN PADA', text2='DATABASE', text3='RASPBERRY')
                time.sleep(1.2)
                lcd_.teks(text1='HARAP', text2='RESTART', text3='RASPBERRY')
                time.sleep(1.2)
                lcd_.teks(text1='JIKA PESAN INI', text2='SELALU MUNCUL')
                time.sleep(1.2)
                lcd_.teks(text1='SEGERA', text2='HUBUNGI', text3='DISKOMINFO')
                time.sleep(1.2)
                # print 'KESALAHAN PADA DATABASE RASPBERRY'
                # print 'HARAP RESTART RASPBERRY'
                # print 'JIKA PESAN INI SELALU MUNCUL, SEGERA HUBUNGI DISKOMINFO'
            
        else :
            lcd_.teks(text1='PERIKSA APAKAH', text2='MESIN TERDAFTAR', text3='DI DISKOMINFO')
            time.sleep(1.2)
            lcd_.teks(text1='PERIKSA KEMBALI', text2='KONEKSI MESIN', text3='DENGAN RASPBERRY')
            time.sleep(1.2)
            # print 'PERIKSA APAKAH MESIN SUDAH TERDAFTAR DI DISKOMINFO'
            # print 'PERIKSA KEMBALI KONEKSI MESIN DENGAN RASPBERRY'
# 

#Fungsi Utama
def play(ip_address) :
    # save_macaddress()
    _MainProgram = MainProgram(ip_address)
    try :
        trigger_api = API().get_server(api['Trigger'])[0]
        trigger     = trigger_api['status']
        spesific_date = trigger_api['patokantanggal']
        spesific_instansi = trigger_api['instansi_id']
    except Exception :
        trigger_api     = 'ServerConnectionError'
    
    try :
        if _MainProgram.is_mesin_registered :
            _MainProgram.management_admin()
            _MainProgram.status_data()
            if trigger is 1 :
                # print 'main'
                _MainProgram.send_attendance()
                _MainProgram.management_employee()
                _MainProgram.clear_absensi()
            elif trigger is 2 :
                _MainProgram.validasi_user()
            elif trigger is 3 :
                try:
                    version     = (API().get_server(api['Versi']))['version']
                except Exception :    
                    version     = 'ServerConnectionError'

                if RpiDatabase().is_version_same(version):
                    lcd_.teks(text1='RASPBERRY', text2='SUDAH', text3='TERUPDATE')
                    time.sleep(1.2)
                else :
                    update(version)
            elif trigger is 4 :
                if RpiDatabase().is_table_zero('attendance') :
                    RpiDatabase().truncate('attendance')
                    lcd_.teks(text1='MENGHAPUS', text2='DATA', text3='ATTENDANCE')
                    time.sleep(1.2)
                    run('sudo reboot', shell=True)
                else :
                    lcd_.teks(text1='DATA ATTENDANCE', text2='KOSONG')
                    time.sleep(1.2)
            elif trigger is 5 :
                if spesific_instansi == skpd :
                    _MainProgram.spesific_send_attendance(spesific_date)
                    _MainProgram.management_employee()
                else :
                    lcd_.teks(text2='MENUNGGU', text3='HARAP SABAR')
                    time.sleep(1.2)
            elif trigger_api is 'ServerConnectionError' :
                raise Exception
        else :
            lcd_.teks(text1='PERIKSA APAKAH', text2='MESIN TERDAFTAR')
            time.sleep(1.2)
            lcd_.teks(text1='JIKA PESAN INI', text2='SELALU MUNCUL')
            time.sleep(1.2)
            lcd_.teks(text1='SEGERA', text2='HUBUNGI', text3='DISKOMINFO')
            time.sleep(1.2)
    except Exception as error:
        logger.error(error)
        # print error
        # print 'error new_main_program'
#
    

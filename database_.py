from subprocess import check_call as run
import os
import mysql.connector
import xml.etree.ElementTree as ET
import time
import requests
import json
import string
import socket
import httplib, urllib, urllib2
import re
import check_connection
import getDataFinger
import lcd_
import instansi_id

config = {
	'user': 'root',
	'password': 'eabsen.kalselprov.go.id',
	'host': 'localhost',
	'database': 'data_finger',
	'raise_on_warnings': True,

}

URL = {
		'ATTENDACE' 	: 'http://eabsen.kalselprov.go.id/api/attendance',
		'AMBILFINGER' 	: 'http://eabsen.kalselprov.go.id/api/ambilfinger/%s',
		'TRIGGER' 		: 'http://eabsen.kalselprov.go.id/api/triger',
		'CEKPEGAWAI' 	: 'http://eabsen.kalselprov.go.id/api/cekpegawai',
		'CEKADMIN' 		: 'http://eabsen.kalselprov.go.id/api/admin/finger',
		'AMBILMAC'		: 'http://eabsen.kalselprov.go.id/api/macaddress',
		'CEKIDPEGAWAI'	: 'http://eabsen.kalselprov.go.id/api/cekpegawaidata/%s',
		'CEKIDADMIN'	: 'http://eabsen.kalselprov.go.id/api/admin/finger/%s',
        'CEKVERSI'	    : 'http://eabsen.kalselprov.go.id/api/version',
        'ERRORUSER'     : 'http://eabsen.kalselprov.go.id/api/logerror'
}

SQL_SYNTAX = {
				'ADDPEGAWAI' 	: 'INSERT INTO pegawai (user_pin2, user_name, mac_) VALUES (%s, %s, %s)',
				'ADDADMIN' 		: 'INSERT INTO pegawaiAdmin (user_pin2, user_name, mac_) VALUES (%s, %s, %s)',
				'FINDMAC'		: 'SELECT mac_ FROM macaddress WHERE mac_ = (%s)',
				'CHECKATTENDACE': 'SELECT COUNT(*) FROM attendance WHERE mac_ = (%s)',
				'ADDATTENDANCE'	: 'INSERT INTO attendance (user_pin, mac_) VALUES (%s, %s)',
				'CHECKPEGAWAI'	: 'SELECT COUNT(*) FROM pegawai WHERE mac_ = (%s)',
				'CHECKADMIN'	: 'SELECT COUNT(*) FROM pegawaiAdmin WHERE mac_ = (%s)',
				'TRUNCATE'		: 'TRUNCATE TABLE attendance',
				'CHECKMAC'		: 'SELECT COUNT(*) FROM macaddress',
				'ADDMAC'		: 'INSERT INTO macaddress (mac_) VALUES (%s)',
				'DELETEPEGAWAI'	: 'DELETE FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
				'DELETEADMIN'	: 'DELETE FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
				'FINDALLADMIN'	: 'SELECT user_pin2 FROM pegawaiAdmin WHERE mac_ = (%s)',
				'FINDADMIN'		: 'SELECT user_pin2 FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
				'FINDPEGAWAI'	: 'SELECT user_pin2 FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDALLPEGAWAI': 'SELECT user_pin2 FROM pegawai WHERE mac_ = (%s)',
                'CHECKVERSION'  : 'SELECT version FROM version',
                'UPDATEVERSION' : 'UPDATE version SET version = %s',
                'ADDVERSION'    : 'INSERT INTO version (version) VALUES = (%s)'
}


# Fungsi Enkripsi
def encrypt(data):
    key = 'D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+12%'
    textASCII = [ord(x) for x in data]
    keyASCII = [ord(x) for x in key]
    encASCII = [(41+((x+y)%26)) for x, y in zip (textASCII, keyASCII)]
    encText = ''.join(chr(x) for x in encASCII)
    return encText

# Fungsi post
def requestPOST (URL, header, payload) :
    try:
        r = requests.post(URL, headers=header, json=payload)
        return r
    except requests.exceptions.RequestException as err:
        print err
        lcd_.printLCD('Request Exception','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.Timeout as err:
        print err
        lcd_.printLCD('Timeout','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.ConnectionError as err:
        print err
        lcd_.printLCD('Connection Error','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.HTTPError as err:
        print err
        lcd_.printLCD('HTTP error','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.ConnectTimeout as err:
        print err
        lcd_.printLCD('Timeout','Trying To Connect').lcd_status()
        return None

# Fungsi get
def requestGET (URL) :
    try:
        r = requests.get(URL, timeout=5)
        return r
    except requests.exceptions.RequestException as err:
        print err
        lcd_.printLCD('Request Exception','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.Timeout as err:
        print err
        lcd_.printLCD('Timeout','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.ConnectionError as err:
        print err
        lcd_.printLCD('Connection Error','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.HTTPError as err:
        print err
        lcd_.printLCD('HTTP error','Trying To Connect').lcd_status()
        return None
    except requests.exceptions.ConnectTimeout as err:
        print err
        lcd_.printLCD('Timeout','Trying To Connect').lcd_status()
        return None

# Fungsi Parsing Data Finger
def parsingFromFinger(data):
    while data is not None or data:
        try :
            parsed = ET.fromstring(data)
            return parsed
        except ET.ParseError as err :
            return None
        except IndexError as err:
            return None
        except ValueError as err:
            return None
    else :
        return None

# Fungsi Parsing Json
def loadJSON(data):
    while data is not None or data:
        try:
            JSONloaded = json.loads(data.content)
            return JSONloaded, True
        except ValueError as err:
                return err, False
        except IndexError as err:
                return err, False
    else:
        return data, False

def cekPegFinger(tujuan, alamat, comKey, ID):
    cekUserFinger = None
    while cekUserFinger is None:
        cekUserFinger = parsingFromFinger(getDataFinger.getUserInfo(tujuan, alamat, comKey, ID).get())
    if len(cekUserFinger) == 0:
        return False
    elif len(cekUserFinger) == 1:
        if str(ID) == cekUserFinger[0][6].text:
            return True
        else :
            return False
# def regisTemplate(dataTemplate, fingerID) :

macFinger = None

def addMacToLocalHost():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    if check_connection.internet.check() :
        getMac = [None,False]
        jumlahMacServ = 0
        while not getMac[1]:
            getMac = loadJSON(requestGET(URL['AMBILMAC']))
        jumlahMacServ = len(getMac[0])
        print 'Jumlah MAC Di Server %s' % jumlahMacServ

        cursor.execute(SQL_SYNTAX['CHECKMAC'])
        fetch = cursor.fetchone()
        jumlahMacLoc = fetch[0]
        print 'Jumlah MAC Di LocalHost %s' % jumlahMacLoc
        selisih = jumlahMacServ - jumlahMacLoc
        print 'Selisih %s' % selisih
        if selisih > 0 :
            for dataMac in range (jumlahMacLoc, jumlahMacServ):
                mac = getMac[0][dataMac]['macaddress']
                print '%s. %s Ditambahkan Ke LocalHost' % (dataMac+1, mac)
                cursor.execute(SQL_SYNTAX['ADDMAC'], (mac,))
                cnx.commit()

def clearDataLog(tujuan, alamat, cursor):
    print 'Clear Log'
    lcd_.printLCD('Clear Log',' ').lcd_status()
    cursor.execute(SQL_SYNTAX['TRUNCATE'])
    getDataFinger.clearData(tujuan, alamat, 0,3).get()
    time.sleep(10)
    print 'Restarting...'
    lcd_.printLCD('Restarting','...').lcd_status()
    run('sudo reboot', shell=True)

def clone():
    SRC = '/home/pi/finger'
    CMD = {
            'REMOVESOURCE'  : 'sudo rm -rf %s',
            'CLONETOSOURCE' : 'sudo git clone https://github.com/Nat4Lia/finger.git %s',
            'COPYTOETC'     : 'sudo cp -R /home/pi/finger /etc/',
            'REBOOT'        : 'sudo reboot'
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    if check_connection.internet.check() :
        trigger = [None,False]
        while not trigger[1] :
            time.sleep(30)
            trigger = loadJSON(requestGET(URL['TRIGGER']))
        print 'Trigger %s' % trigger[0][0]['status']
        if trigger[0][0]['status'] is 3 :
            getVersion = [None, False]
            while not getVersion[1]:
                getVersion = loadJSON(requestGET(URL['CEKVERSI']))
            print getVersion
            versionSer = getVersion[0]['version']
            print 'Versi server %s' % versionSer
            cursor.execute(SQL_SYNTAX['CHECKVERSION'])
            fetch = cursor.fetchone()
            versionLoc = fetch[0]
            print 'versi local %s' % versionLoc
            if versionLoc != versionSer :
                if os.path.isdir(SRC) :
                    print os.path.isdir(SRC)
                    run(CMD['REMOVESOURCE'] % SRC,shell=True)
                    run(CMD['CLONETOSOURCE'] % SRC,shell=True)
                    run(CMD['COPYTOETC'], shell=True)
                    cursor.execute(SQL_SYNTAX['UPDATEVERSION'], (versionSer,))
                    cnx.commit()
                else :
                    print os.path.isdir(SRC)
                    run(CMD['CLONETOSOURCE'] % SRC,shell=True)
                    run(CMD['COPYTOETC'], shell=True)
                    cursor.execute(SQL_SYNTAX['ADDVERSION'], (versionSer,))
                    cnx.commit()
                print 'Updating to Version %s' % versionSer
                lcd_.printLCD('Updating to','Version %s' % versionSer).lcd_status()
                time.sleep(5)
                run(CMD['REBOOT'], shell=True)
class inisialisasi:
    def __init__ (self, tujuan, alamat):
        global macFinger
        self.tujuan = tujuan
        self.alamat = alamat
        self.alamathttp = 'http://%s' % alamat
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor(buffered=True)
        self.koneksifinger = check_connection.onCheck(tujuan, self.alamathttp, 5).check()
        self.koneksiinternet = check_connection.internet.check()
        macFinger = getDataFinger.getOption(tujuan, alamat, 0, 'MAC').get()

    def checkMac(self):
        global macFinger
        print 'Check Mac %s is Already Registered' % macFinger
        self.cursor.execute(SQL_SYNTAX['FINDMAC'], (macFinger,))
        macLocal = self.cursor.fetchone()
        print 'Mac %s Terdaftar' % macLocal
        if macLocal is None:
            lcd_.printLCD('Alat Fingerprint','Tidak Terdaftar').lcd_status()
            return False
        else:
            return True

class proses(inisialisasi):
    def __init__ (self, tujuan, alamat):
        inisialisasi.__init__(self, tujuan, alamat)
        self.checkMac = inisialisasi.checkMac(self)

    def sendLogToServer(self):
        global macFinger
        if self.koneksifinger & self.koneksiinternet :
            print 'Mengambil Data Log Dari Fingerprint'
            lcd_.printLCD('Mengambil Data','Absensi Fingerprint').lcd_status()
            dataLog = None
            jumlahDataLog = 0
            print 'Status Check Mac %s' % self.checkMac
            if self.checkMac:
                counter = 0
                while dataLog is None :
                    data = getDataFinger.getAttLog(self.tujuan, self.alamat, 0,'All').get()
                    try :
                        dataLog = ET.fromstring(data)
                    except ET.ParseError as err :
                        clearDataLog(self.tujuan, self.alamat, self.cursor)
                    except IndexError as err:
                        clearDataLog(self.tujuan, self.alamat, self.cursor)
                    except ValueError as err:
                        clearDataLog(self.tujuan, self.alamat, self.cursor)
                jumlahDataLog = len(dataLog)
                print 'Jumlah Data Log %s' % jumlahDataLog

                self.cursor.execute(SQL_SYNTAX['CHECKATTENDACE'], (macFinger,))
                fetch = self.cursor.fetchone()
                jumlahLogLocal = fetch[0]
                print 'Jumlah Data Log Local %s' % jumlahLogLocal


                selisih = jumlahDataLog - jumlahLogLocal
                print 'Selisih Data Log %s' % selisih
                totalUpload = 0
                if selisih > 0:
                    lcd_.printLCD('Ditemukan','%s Data Record' % selisih).lcd_status()
                    for data in range (jumlahLogLocal, jumlahDataLog):
                        ID_INSTANSI     = instansi_id.ID_INSTANSI
                        PIN             = dataLog[data][0].text
                        MAC             = macFinger
                        tanggal, jam    = dataLog[data][1].text.split(' ')
                        s_verified      = dataLog[data][2].text
                        s_status        = dataLog[data][3].text

                        encryptText = str(jam)+str(tanggal)+str(PIN)+str(ID_INSTANSI)+str(s_status)
                        encryption = encrypt(encryptText)
                        print 'Data Yang Dikirim '
                        print 'user id  : %s' % PIN
                        print 'status   : %s' % s_status
                        print 'instansi : %s' % ID_INSTANSI
                        print 'jam      : %s' % jam
                        print 'tanggal  : %s' % tanggal
                        print 'token    : %s' % encryption

                        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
                        payload = {'status' : s_status, 'instansi' : ID_INSTANSI, 'jam' : jam, 'tanggal' : tanggal, 'user_id' : PIN, 'token' : encryption }

                        statusCode = None
                        while statusCode is not 200:
                            time.sleep(2)
                            print 'Mengirim Log Ke Server'
                            statusCode = requestPOST(URL['ATTENDACE'], headers, payload).status_code
                            print 'status pengiriman %s' % statusCode

                        if statusCode is 200:
                            self.cursor.execute(SQL_SYNTAX['ADDATTENDANCE'], (PIN, MAC,))
                            totalUpload += 1
                            lcd_.printLCD('Upload','Sukses').lcd_status()
                            lcd_.printLCD('Uploading...','%s Data' % totalUpload).lcd_status()
                            print 'Updating %s Data, ID = %s, Jam = %s' % (totalUpload, PIN, jam)
                            print 'Upload Sukses'
                            self.cnx.commit()
                            if totalUpload == selisih :
                                lcd_.printLCD('Success Uploading','%s Data' % totalUpload).lcd_status()
                                print 'Success Updating %s Data' % totalUpload

                else:
                    lcd_.printLCD('Tidak Ada Data','Absensi Baru').lcd_status()

    def setUser(self):
        if self.koneksifinger & self.koneksiinternet :
            print 'Manajemen User Fingerprint'
            trigger = [None,False]
            while not trigger[1] :
                time.sleep(30)
                trigger = loadJSON(requestGET(URL['TRIGGER']))
            print 'Trigger %s' % trigger[0][0]['status']
            if trigger[0][0]['status'] is 1 :
                lcd_.printLCD('Config User','Fingerprint').lcd_status()
                print 'Cek Jumlah Pegawai di Tabel dengan Mac %s ' % macFinger
                self.cursor.execute(SQL_SYNTAX['CHECKPEGAWAI'], (macFinger,))
                fetch = self.cursor.fetchone()
                jumlahPegLoc = fetch[0]
                print 'Jumlah Pegawai Di LocalHost %s' % jumlahPegLoc
                listPegawai = [None,False]
                while not listPegawai[1]:
                    listPegawai = loadJSON(requestGET(URL['CEKPEGAWAI']))
                jumlahPegSer = len(listPegawai[0])
                print 'Jumlah Pegawai di Server %s' % jumlahPegSer
                totalNewPeg = 0
                selisih = jumlahPegSer - jumlahPegLoc
                print 'Selisih %s' % selisih
                if selisih > 0 :
                    lcd_.printLCD('Ditemukan %s' % selisih,'Baru').lcd_status()
                    for pegawai in range (0, jumlahPegSer):
                        ID =  listPegawai[0][pegawai]['id']
                        NAMA = listPegawai[0][pegawai]['nama'].replace("'"," ")
                        self.cursor.execute(SQL_SYNTAX['FINDPEGAWAI'], (ID, macFinger,))
                        cekPegLoc = self.cursor.fetchone()
                        print 'Cek Pegawai %s di LocalHost' % ID
                        if cekPegLoc is None or not cekPegFinger(self.tujuan, self.alamat, 0, ID):
                            hapusUser = parsingFromFinger(getDataFinger.delUser(self.tujuan, self.alamat, 0, ID).delete())
                            print 'Menghapus User %s di fingerprint' % (ID)
                            self.cursor.execute(SQL_SYNTAX['DELETEPEGAWAI'], (ID, macFinger,))
                            self.cnx.commit()
                            print 'Menghapus User %s di localhost' % (ID)
                            fingerPegawai = [None,False]
                            while not fingerPegawai[1]:
                                time.sleep(0.7)
                                lcd_.printLCD('Mengambil Data','Fingerprint').lcd_status()
                                print 'Mencoba Mengambil Data Finger %s ' % NAMA
                                fingerPegawai = loadJSON(requestGET(URL['AMBILFINGER'] % ID))
                            else :
                                setUser = None
                                while setUser is None:
                                    setUser = parsingFromFinger(getDataFinger.setUserInfo(self.tujuan, self.alamat, 0, NAMA, ID).get())
                                print '%s Mendaftarkan ID : %s, Nama : %s ke fingerprint' % (setUser[0][1].text, ID, NAMA)
                                lcd_.printLCD('Mendaftarkan Ke','Fingerprint').lcd_status()
                                status=[None,None]
                                if setUser[0][1].text == 'Successfully!':
                                    for fingerID in range (0,2):
                                        pegawai_id      = fingerPegawai[0][fingerID]['pegawai_id']
                                        size            = fingerPegawai[0][fingerID]['size']
                                        valid           = fingerPegawai[0][fingerID]['valid']
                                        finger_template = fingerPegawai[0][fingerID]['templatefinger']
                                        statusSetTemplate = None
                                        while statusSetTemplate is None:
                                            print 'Mendaftarkan Finger ID %s' % fingerID
                                            lcd_.printLCD('Mendaftarkan','Finger ID %s' % fingerID).lcd_status()
                                            statusSetTemplate = parsingFromFinger(getDataFinger.setUserTemplate(self.tujuan, self.alamat, 0, pegawai_id, fingerID, size, valid, finger_template).get())
                                        status[fingerID] = statusSetTemplate[0][1].text
                                if (status[0] and status[1]) == 'Successfully!':
                                    self.cursor.execute(SQL_SYNTAX['ADDPEGAWAI'], (ID, NAMA, macFinger,))
                                    self.cnx.commit()
                                    totalNewPeg += 1
                                    print 'Sukses menambahkan template finger %s' % NAMA
                                    lcd_.printLCD('Update','%s Pegawai Baru' % totalNewPeg).lcd_status()
                                else:
                                    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
                                    payload = {'user_id' : ID, 'nama' : NAMA}
                                    time.sleep(3)
                                    if requestPOST(URL['ERRORUSER'], headers, payload).status_code is 200:
                                        lcd_.printLCD('User %s' % ID,'Error').lcd_status()
                                        print 'User %s Gagal Terdaftar' % ID
                else:
                    lcd_.printLCD('Tidak Ada Update','Pegawai Baru').lcd_status()

            elif trigger[0][0]['status'] is 2:
                print 'Cek Jumlah Pegawai Di LocalHost'
                self.cursor.execute(SQL_SYNTAX['FINDALLPEGAWAI'], (macFinger,))
                fetch = self.cursor.fetchall()
                jumlahPegLoc = len(fetch)
                print 'Jumlah Pegawai Di LocalHost %s' % jumlahPegLoc

                for pegawai in range(0, jumlahPegLoc):
                    idPegLoc = fetch[pegawai][0]
                    cekPegawai = False
                    while not cekPegawai:
                        time.sleep(1.3)
                        cekPegawai = loadJSON(requestGET(URL['CEKIDPEGAWAI'] % idPegLoc))
                        print 'Cek ID Pegawai %s Di API' % idPegLoc
                    if not cekPegawai[0] :
                        hapusTemplate = None
                        hapusUser = None
                        while hapusTemplate is None:
                            hapusTemplate = parsingFromFinger(getDataFinger.deleteTemplate(self.tujuan, self.alamat, 0, idPegLoc).delete())
                        print '%s Menghapus Template User %s' % (hapusTemplate[0][1].text, idPegLoc)
                        while hapusUser is None:
                            hapusUser = parsingFromFinger(getDataFinger.delUser(self.tujuan, self.alamat, 0, idPegLoc).delete())
                        print '%s Menghapus User %s' % (hapusUser[0][1].text, idPegLoc)
                        self.cursor.execute(SQL_SYNTAX['DELETEPEGAWAI'], (idPegLoc, macFinger,))
                        self.cnx.commit()
                        lcd_.printLCD('Pegawai %s' % idPegLoc,'Dihapus').lcd_status()

    def setAdmin(self):
        if self.koneksifinger & self.koneksiinternet :
            print 'Manajemen Admin Fingerprint'
            trigger = [None,False]
            while not trigger [1]:
                time.sleep(30)
                trigger = loadJSON(requestGET(URL['TRIGGER']))
            print 'Trigger %s' % trigger[0][0]['status']
            if trigger[0][0]['status'] is 1 :
                print 'Cek Jumlah Admin di Tabel dengan Mac %s ' % macFinger
                self.cursor.execute(SQL_SYNTAX['CHECKADMIN'], (macFinger,))
                fetch = self.cursor.fetchone()
                jumlahAdmLoc = fetch[0]
                print 'Jumlah Admin Di LocalHost %s' % jumlahAdmLoc

                listAdmin = [None,False]
                while not listAdmin[1] :
                    listAdmin = loadJSON(requestGET(URL['CEKADMIN']))
                jumlahAdmSer = len(listAdmin[0])
                print 'Jumlah Admin Di Server %s' % jumlahAdmSer

                selisih = jumlahAdmSer - jumlahAdmLoc
                print 'Selisih %s' % selisih

                if selisih > 0:
                    lcd_.printLCD('Menambahkan Admin','Fingerprint').lcd_status()
                    for admin in range(0, jumlahAdmSer):
                        ID = listAdmin[0][admin]['id']
                        print 'ID %s Akan Dijadikan Admin' % ID
                        self.cursor.execute(SQL_SYNTAX['FINDADMIN'], (ID, macFinger,))
                        isiAdmin = self.cursor.fetchone()
                        self.cursor.execute(SQL_SYNTAX['FINDPEGAWAI'], (ID, macFinger,))
                        isiPegawai = self.cursor.fetchone()
                        print isiAdmin, isiPegawai[0]

                        if ((ID == isiPegawai[0]) & (isiAdmin is None)) :
                            print 'Mengubah Pegawai %s Menjadi Admin' % ID
                            hapusTemplate = None
                            hapusUser = None
                            while hapusTemplate is None:
                                hapusTemplate = parsingFromFinger(getDataFinger.deleteTemplate(self.tujuan, self.alamat, 0, ID).delete())
                            print '%s Menghapus Template User %s' % (hapusTemplate[0][1].text, ID)
                            while hapusUser is None:
                                hapusUser = parsingFromFinger(getDataFinger.delUser(self.tujuan, self.alamat, 0, ID).delete())
                            print '%s Menghapus User %s' % (hapusUser[0][1].text, ID)
                            NAMA = listAdmin[0][admin]['nama'].replace("'"," ")
                            fingerPegawai = [None,False]
                            while not fingerPegawai[1]:
                                time.sleep(3.3)
                                print 'Mencoba Mengambil Data Finger Admin %s ' % NAMA
                                fingerPegawai = loadJSON(requestGET(URL['AMBILFINGER'] % ID))
                            else:
                                setUser = None
                                while setUser is None:
                                    setUser = parsingFromFinger(getDataFinger.setAdminUser(self.tujuan, self.alamat, 0, NAMA, ID).get())
                                print '%s Mendaftarkan ID : %s, Nama : %s ke fingerprint sebagai Admin' % (setUser[0][1].text, ID, NAMA)
                                status=['','']
                                if setUser[0][1].text == 'Successfully!':
                                    for fingerID in range (0,2):
                                        pegawai_id      = fingerPegawai[0][fingerID]['pegawai_id']
                                        size            = fingerPegawai[0][fingerID]['size']
                                        valid           = fingerPegawai[0][fingerID]['valid']
                                        finger_template = fingerPegawai[0][fingerID]['templatefinger']
                                        statusSetTemplate = None
                                        while statusSetTemplate is None:
                                            statusSetTemplate = parsingFromFinger(getDataFinger.setUserTemplate(self.tujuan, self.alamat, 0, pegawai_id, fingerID, size, valid, finger_template).get())
                                        status[fingerID] = statusSetTemplate[0][1].text
                                        print 'Template %s Added' % status[fingerID]
                                if (status[0] and status[1]) == 'Successfully!':
                                    self.cursor.execute(SQL_SYNTAX['ADDPEGAWAI'], (ID, NAMA, macFinger,))
                                    self.cursor.execute(SQL_SYNTAX['ADDADMIN'], (ID, NAMA, macFinger,))
                                    self.cnx.commit()
                                    lcd_.printLCD('Sukses Menambahkan','Admin').lcd_status()
                elif selisih <= 0:
                    print 'Cek ID Admin di Tabel dengan Mac %s ' % macFinger
                    self.cursor.execute(SQL_SYNTAX['FINDALLADMIN'], (macFinger,))
                    fetch = self.cursor.fetchall()

                    for cekID in range (0, jumlahAdmLoc):
                        ID = fetch[cekID][0]
                        print 'Cek ID %s di API Cek Admin' % ID
                        cekAdmin = [None,False]
                        while not cekAdmin[1]:
                            time.sleep(1.3)
                            cekAdmin = loadJSON(requestGET(URL['CEKIDADMIN'] % ID))
                        if not cekAdmin[0] :
                            lcd_.printLCD('Menghapus Admin','Fingerprint').lcd_status()
                            print 'ID %s tidak terdaftar sebagai Admin' % ID
                            cekPegawai = [None,False]
                            while not cekPegawai[1]:
                                time.sleep(1.3)
                                cekPegawai = loadJSON(requestGET(URL['CEKIDADMIN'] % ID))
                            ID =  cekPegawai[0][0]['pegawai_id']
                            NAMA = cekPegawai[0][0]['nama'].replace("'"," ")
                            print 'Mengubah %s menjadi User' % NAMA
                            fingerPegawai = [None,False]
                            while not fingerPegawai[1]:
                                lcd_.printLCD('Mengambil Data','Fingerprint').lcd_status()
                                print 'Mencoba Mengambil Data Finger %s ' % NAMA
                                time.sleep(3.3)
                                fingerPegawai = loadJSON(requestGET(URL['AMBILFINGER'] % ID))
                            else :
                                hapusTemplate = None
                                hapusUser = None
                                while hapusTemplate is None:
                                    hapusTemplate = parsingFromFinger(getDataFinger.deleteTemplate(self.tujuan, self.alamat, 0, ID).delete())
                                print '%s Menghapus Template User %s' % (hapusTemplate[0][1].text, ID)
                                while hapusUser is None:
                                    hapusUser = parsingFromFinger(getDataFinger.delUser(self.tujuan, self.alamat, 0, ID).delete())
                                print '%s Menghapus User %s' % (hapusUser[0][1].text, ID)
                                setUser = None
                                while setUser is None:
                                    setUser = parsingFromFinger(getDataFinger.setUserInfo(self.tujuan, self.alamat, 0, NAMA, ID).get())
                                print '%s Mendaftarkan ID : %s, Nama : %s ke fingerprint' % (setUser[0][1].text, ID, NAMA)
                                status=[None,None]
                                if setUser[0][1].text == 'Successfully!':
                                    for fingerID in range (0,2):
                                        pegawai_id      = fingerPegawai[0][fingerID]['pegawai_id']
                                        size            = fingerPegawai[0][fingerID]['size']
                                        valid           = fingerPegawai[0][fingerID]['valid']
                                        finger_template = fingerPegawai[0][fingerID]['templatefinger']
                                        statusSetTemplate = None
                                        while statusSetTemplate is None:
                                            statusSetTemplate = parsingFromFinger(getDataFinger.setUserTemplate(self.tujuan, self.alamat, 0, pegawai_id, fingerID, size, valid, finger_template).get())
                                        status[fingerID] = statusSetTemplate[0][1].text
                                if (status[0] and status[1]) == 'Successfully!':
                                    lcd_.printLCD('Sukses Menghapus','Admin').lcd_status()

    def clearLog(self):
        if self.koneksifinger :
            print 'Menghapus Log Di Fingerprint'
            if self.checkMac:
                dataLog = None
                while dataLog is None :
                    dataLog = parsingFromFinger(getDataFinger.getAttLog(self.tujuan, self.alamat, 0,'All').get())
                jumlahDataLog = len(dataLog)
                print 'Jumlah Data Log %s' % jumlahDataLog

                self.cursor.execute(SQL_SYNTAX['CHECKATTENDACE'], (macFinger,))
                fetch = self.cursor.fetchone()
                jumlahLogLocal = fetch[0]
                print 'Jumlah Data Log Local %s' % jumlahLogLocal

                if (jumlahLogLocal & jumlahDataLog) >= 100000 :
                    print 'Menghapus Log di LocalHost'
                    lcd_.printLCD('Menghapus Log','Fingerprint').lcd_status()
                    self.cursor.execute(SQL_SYNTAX['TRUNCATE'])
                    clear = parsingFromFinger(getDataFinger.clearData(self.tujuan, self.alamat, 0,3).get())
                    time.sleep(10)
                    if clear is None:
                        lcd_.printLCD('Clear Log','Successfully!').lcd_status()



# cekPegFinger('Finger-A','10.10.10.10:80',0,172)
# P = proses('Finger A','10.10.10.10:80')
#
# addMacToLocalHost()
# P.setUser()
# P.setAdmin()
# proses('Finger A','10.10.10.10:80').setAdmin()

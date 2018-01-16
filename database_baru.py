import Web_Access as Server
import Local_Access as Local
import Fingerprint_Access as Finger
import instansi_id
import time
import lcd_ as cetak
from subprocess import check_call as run
import os

FungsiLocal = Local.Localhost()

def resetall(usealamat):
    if Server.load('Trigger',None) is 4:
        for alamat in usealamat:
            cetak.printLCD ('Reset Semua Data','').lcd_status()
            JUMLAHPEGAWAIFINGER = Finger.jumlahpegawai(alamat, usealamat[alamat])
            JUMLAHDATAABSENSI   = len(Finger.ambildataabsensi(alamat, usealamat[alamat]))
            if JUMLAHDATAABSENSI or JUMLAHPEGAWAIFINGER != 0:
                Finger.hapusabsensi(alamat, usealamat[alamat])
                Finger.hapussemua(alamat, usealamat[alamat])
                FungsiLocal.hapussemua()
                cetak.printLCD ('Reseting %s' % alamat,'').lcd_status()
                time.sleep(30)

def clone():
    SRC = '/home/pi/finger'
    CMD = {
            'REMOVESOURCE'  : 'sudo rm -rf %s',
            'CLONETOSOURCE' : 'sudo git clone https://github.com/Nat4Lia/finger.git %s',
            'COPYTOETC'     : 'sudo cp -R /home/pi/finger /etc/',
            'REBOOT'        : 'sudo reboot'
    }

    if Server.load('Trigger',None) is 3 :
        version = Server.load('Update',None)
        if FungsiLocal.cekversion(version) :
            cetak.printLCD ('Updating...','').lcd_status()
            if os.path.isdir(SRC) :
                run(CMD['REMOVESOURCE'] % SRC,shell=True)
                run(CMD['CLONETOSOURCE'] % SRC,shell=True)
                run(CMD['COPYTOETC'], shell=True)
                FungsiLocal.updateversion(version)
            else :
                run(CMD['CLONETOSOURCE'] % SRC,shell=True)
                run(CMD['COPYTOETC'], shell=True)
                FungsiLocal.tambahversion(version)
            cetak.printLCD('Update ke versi','%s' % version).lcd_status()
            time.sleep(5)
            cetak.printLCD('Restarting Raspberry','...').lcd_status()
            run(CMD['REBOOT'], shell=True)

def encrypt(data):
    key = 'D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121'
    textASCII = [ord(x) for x in data]
    keyASCII = [ord(x) for x in key]
    encASCII = [(41+((x+y)%26)) for x, y in zip (textASCII, keyASCII)]
    encText = ''.join(chr(x) for x in encASCII)
    return encText

def hapuspegawai(tujuan, alamat, pegawaiid, mac):
    while True:
        Finger.hapuspegawai(tujuan, alamat, pegawaiid)
        if not Finger.cekpegawai(tujuan, alamat, pegawaiid) and not FungsiLocal.hapuspegawai(pegawaiid, mac):
            return True
        else:
            return False

def daftarpegawai(tujuan, alamat, pegawaiid, nama, mac):
    try:
        daftarfinger    = Finger.daftarpegawai(tujuan, alamat, pegawaiid, nama)
        daftarlocal     = FungsiLocal.daftarpegawai(pegawaiid, nama, mac)

        if daftarfinger and daftarlocal:
            return 'Sukses'
        elif daftarfinger and not daftarlocal:
            return 'Finger'
        elif not daftarfinger and daftarlocal:
            return 'Localhost'
        else:
            pass
    except IOError as err:
        print err

def normalizepegawai(tujuan, alamat, mac):
    while True:
        data = FungsiLocal.carisemuapegawai(mac) #Mengambil array localhost
        for pegawai in range (0, len(data)):
            try:
                pegawaiid = data[pegawai][0]
            except IndexError as err:
                print err
            # #Cari ID ke Server
            x = Server.load('CekPegawai',pegawaiid)
            if len(x) is not 0 :
                normal = FungsiLocal.normalizelocalhostpegawai(pegawaiid, mac)
                if len(normal) > 1 :
                    for pegawai in range (0, len(normal)):
                        FungsiLocal.hapuspegawaiid(normal[pegawai][0], mac)
                    while True:
                        if Finger.cekpegawai(tujuan, alamat, pegawaiid):
                            Finger.hapuspegawai(tujuan, alamat, pegawaiid)
                        else:
                            break
                    daftarkan   = daftarpegawai(tujuan, alamat, pegawaiid, x[0]['nama'], mac)

            else:
                while True:
                    if not FungsiLocal.cekpegawai(pegawaiid, mac) and not Finger.cekpegawai(tujuan, alamat, pegawaiid):
                        break
                    else:
                        FungsiLocal.hapuspegawai(pegawaiid, mac)
                        Finger.hapuspegawai(tujuan, alamat, pegawaiid)
        return

def hapusadmin(tujuan, alamat, pegawaiid, mac):
    while True:
        Finger.hapuspegawai(tujuan, alamat, pegawaiid)
        if not Finger.cekpegawai(tujuan, alamat, pegawaiid) and not FungsiLocal.hapusadmin(pegawaiid, mac):
            return True
        else:
            return False

def daftaradmin(tujuan, alamat, adminid, nama, mac):
    try:
        daftarfinger    = Finger.daftaradmin(tujuan, alamat, adminid, nama)
        daftarlocal     = FungsiLocal.daftaradmin(adminid, nama, mac)

        if daftarfinger and daftarlocal:
            return 'Sukses'
        elif daftarfinger and not daftarlocal:
            return 'Finger'
        elif not daftarfinger and daftarlocal:
            return 'Localhost'
        else:
            pass
    except IOError as err:
        print err

def normalizeadmin(tujuan, alamat, mac):
    while True:
        data = FungsiLocal.carisemuaadmin(mac) #Mengambil array localhost
        for pegawai in range (0, len(data)):
            try:
                pegawaiid = data[pegawai][0]
            except IndexError as err:
                print err
            #Cari ID ke Server
            x = Server.load('CekAdmin',pegawaiid)
            if len(x) is not 0 :
                normal = FungsiLocal.normalizelocalhostadmin(pegawaiid, mac)
                if len(normal) > 1 :
                    for pegawai in range (0, len(normal)):
                        FungsiLocal.hapusadminid(normal[pegawai][0], mac)

                    while True:
                        if Finger.cekpegawai(tujuan, alamat, pegawaiid):
                            Finger.hapuspegawai(tujuan, alamat, pegawaiid)
                        else:
                            break
                    daftarkan   = daftaradmin(tujuan, alamat, pegawaiid, x[0]['nama'], mac)

            else:
                while True:
                    if not FungsiLocal.cekadmin(pegawaiid, mac) and not Finger.cekpegawai(tujuan, alamat, pegawaiid):
                        break
                    else:
                        FungsiLocal.hapusadmin(pegawaiid, mac)
                        Finger.hapuspegawai(tujuan, alamat, pegawaiid)
        return

def normalizemac(datalocal, dataserver):
    for listmaclocal in range(0,len(datalocal)):
        try:
            macL = datalocal[listmaclocal][0]
            print macL
            for listmacserver in range(0, len(dataserver)):
                try:
                    macS = dataserver[listmacserver]['macaddress']
                    print macL, macS
                    if macL != macS :
                        FungsiLocal.hapusmac(macL)
                except TypeError as err:
                    print err
                except IndexError as err:
                    print err
                except ValueError as err:
                    print err
        except TypeError as err:
            print err
        except IndexError as err:
            print err
        except ValueError as err:
            print err

def daftarmac():
    DAFTARMACADDRESSSERVER  = Server.load('Macaddress',None)
    JUMLAHMACADDRESSSERVER  = len(DAFTARMACADDRESSSERVER)
    MACLOCAL                = FungsiLocal.cekkesemuamac()
    normalizemac(MACLOCAL, DAFTARMACADDRESSSERVER)
    JUMLAHMACADDRESSLOCAL   = FungsiLocal.cekjumlahmac()
    SELISIHJUMLAHMAC        = JUMLAHMACADDRESSSERVER - JUMLAHMACADDRESSLOCAL
    if SELISIHJUMLAHMAC > 0:
        for DAFTARMAC in range (JUMLAHMACADDRESSLOCAL, JUMLAHMACADDRESSSERVER):
            try:
                MACADDRESS = DAFTARMACADDRESSSERVER[DAFTARMAC]['macaddress']
                FungsiLocal.daftarmac(MACADDRESS)
            except TypeError as err:
                print err
            except IndexError as err:
                print err
            except ValueError as err:
                print err

class Proses:
    def __init__ (self, tujuan, alamat):
        self.tujuan = tujuan
        self.alamat = alamat

    def manajemenuser(self):
        tujuan  = self.tujuan
        alamat  = self.alamat
        mac     = Finger.ambilmacaddress(tujuan, alamat)
        JumlahDaftarBaru    = 0
        jumlahDihapus       = 0
        if FungsiLocal.macterdaftar(mac) :
            cetak.printLCD('Pengaturan Pegawai','Fingerprint').lcd_status()
            if Server.load('Trigger',None) is 1:
                cetak.printLCD('Menambahkan','Pegawai').lcd_status()
                APICEKPEGAWAI          = Server.load('Pegawai',None)
                JUMLAHPEGAWAISERVER     = len(APICEKPEGAWAI)
                JUMLAHPEGAWAIFINGER     = Finger.jumlahpegawai(tujuan, alamat) - FungsiLocal.cekjumlahadmin(mac)
                JUMMLAHPEGAWAILOCAL     = FungsiLocal.cekjumlahpegawai(mac)
                SELISIHJUMLAHPEGAWAI    = JUMLAHPEGAWAISERVER - JUMMLAHPEGAWAILOCAL
                if SELISIHJUMLAHPEGAWAI > 0: #Jika Terdapat Pegawai Baru Di Server
                    #MENGAMBIL DATA ARRAY API
                    for PEGAWAI in range (0, JUMLAHPEGAWAISERVER):
                        #Mengambil ID dan NAMA pegawai
                        try:
                            ID =  APICEKPEGAWAI[PEGAWAI]['id']
                            NAMA = APICEKPEGAWAI[PEGAWAI]['nama'].replace("'"," ")
                        except ValueError as err:
                            print err
                        except TypeError as err:
                            print err
                        #Daftarkan Pegawai
                        try:
                            daftarkan   = daftarpegawai(tujuan, alamat, ID, NAMA, mac)
                            if daftarkan == 'Sukses':
                                JumlahDaftarBaru += 1
                            elif daftarkan == 'Finger':
                                pass
                            elif daftarkan == 'Localhost':
                                pass
                        except IOError as err:
                            print err

                elif SELISIHJUMLAHPEGAWAI < 0 : #Jika Data Di Localhost Tidak Normal
                    cetak.printLCD('Pembaruan Data','Pegawai').lcd_status()
                    normalizepegawai(tujuan, alamat, mac)
                elif JUMMLAHPEGAWAILOCAL != JUMLAHPEGAWAIFINGER:

                    cetak.printLCD('Pembaruan Data','Pegawai').lcd_status()
                    for PEGAWAI in range (0, JUMLAHPEGAWAISERVER):
                        #Mengambil ID dan NAMA pegawai
                        try:
                            ID =  APICEKPEGAWAI[PEGAWAI]['id']
                            NAMA = APICEKPEGAWAI[PEGAWAI]['nama'].replace("'"," ")
                        except ValueError as err:
                            print err
                        except TypeError as err:
                            print err
                        #Daftarkan Pegawai
                        try:
                            daftarkan   = daftarpegawai(tujuan, alamat, ID, NAMA, mac)
                        except IOError as err:
                            print err
                else:
                    pass

                if JumlahDaftarBaru == 0:
                    pass
                    cetak.printLCD('Tidak Ada','Pegawai Baru').lcd_status()
                else:
                    pass
                    cetak.printLCD('%s Pegawai Baru' % JumlahDaftarBaru,'Berhasil Ditambahkan').lcd_status()

            elif Server.load('Trigger',None) is 2:
                APIHAPUSPEGAWAI         = Server.load('HapusPegawai',None)
                JUMLAHPEGAWAIDIHAPUS    = len(APIHAPUSPEGAWAI)
                for PEGAWAI in range (0, JUMLAHPEGAWAIDIHAPUS) :
                    try:
                        ID      = APIHAPUSPEGAWAI[PEGAWAI]['pegawai_id']
                        hapuspegawai(tujuan,  alamat, ID, mac)
                        jumlahDihapus += 1
                    except ValueError as err:
                        print err
                    except TypeError as err:
                        print err

                cetak.printLCD('%s Pegawai' % JumlahDaftarBaru,'Berhasil Dihapus').lcd_status()


        else:
            cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
            time.sleep(3)
            cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()
            time.sleep(3)

    def manajemenadmin(self):
        tujuan  = self.tujuan
        alamat  = self.alamat
        mac     = Finger.ambilmacaddress(tujuan, alamat)
        JumlahDaftarBaru    = 0
        jumlahDihapus       = 0
        if FungsiLocal.macterdaftar(mac) :
            if Server.load('Trigger',None) is 1:
                cetak.printLCD('Menambahkan','Admin').lcd_status()
                APICEKADMIN             = Server.load('Admin',None)
                JUMLAHADMINSERVER       = len(APICEKADMIN)
                JUMLAHADMINFINGER       = Finger.jumlahpegawai(tujuan, alamat) - FungsiLocal.cekjumlahpegawai(mac)
                JUMMLAHADMINLOCAL       = FungsiLocal.cekjumlahadmin(mac)
                SELISIHJUMLAHADMIN      = JUMLAHADMINSERVER - JUMMLAHADMINLOCAL
                if SELISIHJUMLAHADMIN > 0 : #Jika Terdapat ADMIN Baru Di Server
                    #MENGAMBIL DATA ARRAY API
                    for ADMIN in range (0, JUMLAHADMINSERVER):
                        #Mengambil ID dan NAMA ADMIN
                        try:
                            ID =  APICEKADMIN[ADMIN]['id']
                            NAMA = APICEKADMIN[ADMIN]['nama'].replace("'"," ")
                        except ValueError as err:
                            print err
                        except TypeError as err:
                            print err
                        #Daftarkan ADMIN
                        try:
                            daftarkan   = daftaradmin(tujuan, alamat, ID, NAMA, mac)
                            if daftarkan == 'Sukses':
                                JumlahDaftarBaru += 1
                            elif daftarkan == 'Finger':
                                pass
                            elif daftarkan == 'Localhost':
                                pass
                        except IOError as err:
                            print err

                elif SELISIHJUMLAHADMIN < 0: #Jika Data Di Localhost Tidak Normal
                    cetak.printLCD('Pembaruan Data','Admin').lcd_status()
                    normalizeadmin(tujuan, alamat, mac)

                elif JUMMLAHADMINLOCAL != JUMLAHADMINFINGER:
                    cetak.printLCD('Pembaruan Data','Admin').lcd_status()
                    for PEGAWAI in range (0, JUMLAHADMINSERVER):
                        #Mengambil ID dan NAMA pegawai
                        try:
                            ID =  APICEKADMIN[PEGAWAI]['id']
                            NAMA = APICEKADMIN[PEGAWAI]['nama'].replace("'"," ")
                        except ValueError as err:
                            print err
                        except TypeError as err:
                            print err
                        #Daftarkan Pegawai
                        try:
                            daftarkan   = daftaradmin(tujuan, alamat, ID, NAMA, mac)
                        except IOError as err:
                            print err
                else:
                    pass

                if JumlahDaftarBaru == 0:
                    pass
                    cetak.printLCD('Tidak Ada','Admin Baru').lcd_status()
                else:
                    pass
                    cetak.printLCD('%s Admin Baru' % JumlahDaftarBaru,'Berhasil Ditambahkan').lcd_status()

            elif Server.load('Trigger',None) is 2:
                APIHAPUSADMIN         = Server.load('Admin',None)
                JUMLAHADMINDIHAPUS    = len(APIHAPUSADMIN)
                for ADMIN in range (0, JUMLAHADMINDIHAPUS) :
                    try:
                        ID      = APIHAPUSADMIN[ADMIN]['pegawai_id']
                        hapusadmin(tujuan,  alamat, ID, mac)
                        jumlahDihapus += 1
                    except ValueError as err:
                        print err
                    except TypeError as err:
                        print err
                cetak.printLCD('%s Admin' % JumlahDaftarBaru,'Berhasil Dihapus').lcd_status()
        else:
            pass
            cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
            cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()

    def clearlog(self):
        tujuan  = self.tujuan
        alamat  = self.alamat
        mac     = Finger.ambilmacaddress(tujuan, alamat)

        if FungsiLocal.macterdaftar(mac) :
            #Jika Mac Terdaftar
            JUMLAHABSENSIFINGER     = len(Finger.ambildataabsensi(tujuan, alamat))
            JUMLAHABSENSILOCAL      = FungsiLocal.cekjumlahabsensi(mac)
            if (JUMLAHABSENSIFINGER and JUMLAHABSENSILOCAL) >=50000:
                cetak.printLCD('Menghapus data','absensi lama').lcd_status()
                Finger.hapusabsensi(tujuan, alamat)
                FungsiLocal.hapusdataabsensi(mac)
        else:
            cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
            time.sleep(3)
            cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()
            time.sleep(3)


    def kirimdataabsensi(self):
        tujuan  = self.tujuan
        alamat  = self.alamat
        mac     = Finger.ambilmacaddress(tujuan, alamat)

        if FungsiLocal.macterdaftar(mac) :
            cetak.printLCD('Mengambil Data','Absensi').lcd_status()
            DATAABSENSI             = Finger.ambildataabsensi(tujuan, alamat)
            JUMLAHDATAABSENSI       = len(DATAABSENSI)
            JUMLAHDATAABSENSILOCAL  = FungsiLocal.cekjumlahabsensi(mac)
            SELISIHDATAABSENSI      = JUMLAHDATAABSENSI - JUMLAHDATAABSENSILOCAL
            TOTALSUKSESPOST         = 0
            TOTALGAGALPOST          = 0
            if SELISIHDATAABSENSI > 0:
                for DATA in range (JUMLAHDATAABSENSILOCAL, JUMLAHDATAABSENSI):
                    try:
                        IDINSTANSI      = instansi_id.ID_INSTANSI
                        USERPIN         = DATAABSENSI[DATA][0].text
                        TANGGAL, JAM    = DATAABSENSI[DATA][1].text.split(' ')
                        VERIFIKASI      = DATAABSENSI[DATA][2].text
                        STATUS          = DATAABSENSI[DATA][3].text
                        MACADDRESS      = mac

                        encryptText     = str(JAM) + str(TANGGAL) + str(USERPIN) + str(IDINSTANSI) + str(STATUS)
                        encryption      = encrypt(encryptText)

                        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
                        payload = {'status' : STATUS, 'instansi' : IDINSTANSI, 'jam' : JAM, 'tanggal' : TANGGAL, 'user_id' : USERPIN, 'token' : encryption }

                        if Server.POST('KEHADIRAN', headers, payload):
                            FungsiLocal.inputdataabsensi(USERPIN, MACADDRESS)
                            TOTALSUKSESPOST +=1
                            cetak.printLCD('Total Absensi','Berhasil Dikirim %s' % TOTALSUKSESPOST).lcd_status()
                        else:
                            TOTALGAGALPOST +=1
                            cetak.printLCD('Total Absensi','Gagal Dikirim %s' % TOTALGAGALPOST).lcd_status()

                    except TypeError as err:
                        print err
                    except ValueError as err:
                        print err
                    except IndexError as err:
                        print err
            else:
                pass
                cetak.printLCD('Tidak Ada','Absensi Baru').lcd_status()
        else:
            pass
            cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
            time.sleep(3)
            cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()
            time.sleep(3)

    def kirimstatus(self):
        cetak.printLCD('Mengirim Status','Data Raspberry').lcd_status()
        tujuan  = self.tujuan
        alamat  = self.alamat
        mac     = Finger.ambilmacaddress(tujuan, alamat)

        ip                  = alamat.replace(':80','')
        versi               = FungsiLocal.ambilversion()
        jumlahmac           = FungsiLocal.cekjumlahmac()
        jumlahpegawaifinger = Finger.jumlahpegawai(tujuan, alamat) - FungsiLocal.cekjumlahadmin(mac)
        jumlahadminfinger   = Finger.jumlahpegawai(tujuan, alamat) - FungsiLocal.cekjumlahpegawai(mac)
        jumlahabsensifinger = len(Finger.ambildataabsensi(tujuan, alamat))
        jumlahpegawailocal  = FungsiLocal.cekjumlahpegawai(mac)
        jumlahadminlocal    = FungsiLocal.cekjumlahadmin(mac)
        jumlahabsensilocal  = FungsiLocal.cekjumlahabsensi(mac)
        instansiid          = instansi_id.ID_INSTANSI

        encryptText     = str(ip) + str(versi) + str(jumlahmac) + str(jumlahpegawaifinger) + str(jumlahadminfinger) + str(jumlahabsensifinger) + str(jumlahpegawailocal) + str(jumlahadminlocal) + str(jumlahabsensilocal) + str(instansiid)
        encryption      = encrypt(encryptText)
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        payload = {
                     'ip'                  : ip,
                     'versi'               : versi,
                     'jumlahmac'           : jumlahmac,
                     'jumlahpegawaifinger' : jumlahpegawaifinger,
                     'jumlahadminfinger'   : jumlahadminfinger,
                     'jumlahabsensifinger' : jumlahabsensifinger,
                     'jumlahpegawailocal'  : jumlahpegawailocal,
                     'jumlahadminlocal'    : jumlahadminlocal,
                     'jumlahabsensilocal'  : jumlahabsensilocal,
                     'instansi_id'         : instansiid,
                     'token'               : encryption
                    }
        print Server.POST('LOGRASPBERRY', headers, payload)
        if Server.POST('LOGRASPBERRY', headers, payload):
            cetak.printLCD('Berhasil Mengirim','Status Raspberry').lcd_status()
        else:
            cetak.printLCD('Gagal Mengirim','Status Raspberry').lcd_status()

# clearlog(tujuan, '10.10.10.10:80', '00:17:61:11:72:24')
# manajemenuser('Finger A', '10.10.10.10:80')
# normalizepegawai('Finger A', '10.10.10.10:80','00:17:61:11:72:24')
# daftarmac()

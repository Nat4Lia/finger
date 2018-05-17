import requests
import xml.etree.ElementTree as ET
import json
import os
from subprocess import check_call as run
from API import API
from Local_Access import Localhost
import instansi_id
import logging
import lcd_ as tampil
import time

webAPI      = API()
dataLocal   = Localhost()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# create a file handler
handler = logging.FileHandler('Error.log')
handler.setLevel(logging.ERROR)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def encrypt(data):
    key = 'D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121'
    textASCII = [ord(x) for x in data]
    keyASCII = [ord(x) for x in key]
    encASCII = [(41+((x+y)%26)) for x, y in zip (textASCII, keyASCII)]
    encText = ''.join(chr(x) for x in encASCII)
    return encText

def update(version):
        SRC = '/home/pi/finger'
        CMD = {
                'REMOVESOURCE'  : 'sudo rm -rf %s',
                'CLONETOSOURCE' : 'sudo git clone https://github.com/Nat4Lia/finger.git %s',
                'COPYTOETC'     : 'sudo cp -R /home/pi/finger /etc/',
                'REBOOT'        : 'sudo reboot'
        }

        tampil.teks(text1='UPDATE PROGRAM', text2='RASPBERRY')
        time.sleep(1.2)
        if os.path.isdir(SRC) :
            run(CMD['REMOVESOURCE'] % SRC,shell=True)
            run(CMD['CLONETOSOURCE'] % SRC,shell=True)
            run(CMD['COPYTOETC'], shell=True)
            dataLocal.updateversion(version)
        else :
            run(CMD['CLONETOSOURCE'] % SRC,shell=True)
            run(CMD['COPYTOETC'], shell=True)
            dataLocal.tambahversion(version)
        tampil.teks(text1='PROGRAM RASPBERRY', text2='UPDATE', text3='KE VERSI %s' % dataLocal.ambilversion())
        time.sleep(1.2)
        time.sleep(5)
        tampil.teks(text1='RASPBERRY', text2='AKAN MELAKUKAN', text3='RESTART')
        time.sleep(1.2)
        run(CMD['REBOOT'], shell=True)

get = {
        'GetAttLog'         : '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></GetAttLog>',
        'GetUserTemplate'   : '<GetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID></Arg></GetUserTemplate>',
        'GetUserInfo'       : '<GetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></GetUserInfo>',
        'SetUserInfoPass'   : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password>%s</Password><Group>1</Group><Privilege></Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
        'SetUserInfoTem'    : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group>1</Group><Privilege></Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
        'DeleteUser'        : '<DeleteUser><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteUser>',
        'GetAllUserInfo'    : '<GetAllUserInfo><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey></GetAllUserInfo>',
        'SetUserTemplate'   : '<SetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID><Size>%s</Size><Valid>%s</Valid><Template>%s</Template></Arg></SetUserTemplate>',
        'ClearData'         : '<ClearData><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Value xsi:type=\"xsd:integer\">%s</Value></Arg></ClearData>',
        'GetOption'         : '<GetOption><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Name xsi:type=\"xsd:string\">%s</Name></Arg></GetOption>',
        'DeleteTemplate'    : '<DeleteTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteTemplate>',
        'SetAdminUserTem'   : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group></Group><Privilege>14</Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
        'SetAdminUserPass'  : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password>%s</Password><Group></Group><Privilege>14</Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
        'ClearUserPassword' : '<ClearUserPassword><ArgComKey xsi:type="xsd:integer">0</ArgComKey><Arg><PIN xsi:type="xsd:integer">%s</PIN></Arg></ClearUserPassword>'
      }

class metode:

    def __init__ (self, ipAddress):
        self.ipAddress  = ipAddress

    def POST (self, payload):
        try:
            r = requests.post(  'http://%s:80/iWsService' % self.ipAddress,
                                headers = {'Content-Type' : 'text/xml'}, 
                                data    = payload,
                                timeout = 5   )
            # print r.content
            return ET.fromstring(r.content)
            # return None
        except (requests.exceptions.RequestException, ET.ParseError, ValueError, TypeError, IndexError) as err:

            if str(self.ipAddress) == str('10.10.10.10') :
                fingerprintName = 'FINGERPRINT A'
            elif str(self.ipAddress) == str('10.10.10.20') :
                fingerprintName = 'FINGERPRINT B'
            elif str(self.ipAddress) == str('10.10.10.30') :
                fingerprintName = 'FINGERPRINT C'
            elif str(self.ipAddress) == str('10.10.10.40') :
                fingerprintName = 'FINGERPRINT D'
            elif str(self.ipAddress) == str('10.10.10.50') :
                fingerprintName = 'FINGERPRINT E'

            tampil.teks(text1='KONEKSI', 
                    text2=fingerprintName, 
                    text3='TERPUTUS')
            time.sleep(1)
            logger.error(err)
            pass
class Admin(metode):
    jumlahAdmin = 0

    def __init__ (self, tujuan, id, name) :
        self.id = id
        self.name = name.replace("'"," ")
        self.key = webAPI.TEMPLATE(id)
        metode.__init__(self, tujuan)

    def jenisKey(self):
        if self.key :
            if len(self.key[0]['templatefinger']) > 8:
                return 'Template'
            elif len(self.key[0]['templatefinger']) <= 8 and len(self.key[0]['templatefinger']) > 0:
                return 'Password'
        else:
            pass

    def daftar(self):
        result = None
        try :
            if self.cek() is False:
                if self.jenisKey() is 'Template' :
                    registering = self.POST (
                        get['SetAdminUserTem'] % (self.name, self.id)
                    )
                    if registering._children:
                        for key_id, key in enumerate(self.key):
                            registering_Template = self.POST (
                                get['SetUserTemplate'] % (
                                    self.id, 
                                    key_id, 
                                    key['size'],
                                    key['valid'],
                                    key['templatefinger']
                                )
                            )
                            if not registering_Template._children :
                                raise AttributeError, registering_Template
                        result = 'Berhasil'
                    else:
                        result = 'Gagal'

                elif self.jenisKey() is 'Password':
                    registering = self.POST (
                        get['SetAdminUserPass'] % (
                            self.name, 
                            self.key[0]['templatefinger'], 
                            self.id)
                    )
                    if registering._children :
                        result = 'Berhasil'
                    else:
                        result = 'Gagal'

            elif self.cek() is True:
                result = 'Sudah Terdaftar'
        except Exception:
            result = 'Gagal'
        
        finally:
            if result is 'Gagal' : #rollback
                self.hapus()
                return result
            elif result is 'Berhasil' or result is 'Sudah Terdaftar': #return
                return result
 
    def cek(self):
        whoChecked = self.POST (get['GetUserInfo'] % (self.id))
        try:
            if whoChecked._children :
                return True
            else:
                return False
        except Exception:
            pass
        
    def hapus(self):
        result = False
        try:
            while self.cek() is True:
                whoRemoved = self.POST (get['DeleteUser'] % (self.id))
                if whoRemoved._children:
                    result = True
                else:
                    result = False
        except Exception:
            pass
        finally:
            return result

    def update(self):
        try:
            if self.hapus() :
                if self.daftar() == 'Berhasil':
                    return True
                else :
                    return False
            else:
                return False
        except Exception:
            pass
 
class Pegawai(metode):
    jumlahPegawai = 0

    def __init__ (self, tujuan, id, name) :
        self.id = id
        self.name = name.replace("'"," ")
        self.key = webAPI.TEMPLATE(id)
        Pegawai.jumlahPegawai += 1
        metode.__init__(self, tujuan)

    def jenisKey(self):
        if self.key :
            if len(self.key[0]['templatefinger']) > 8:
                return 'Template'
            elif len(self.key[0]['templatefinger']) <= 8 and len(self.key[0]['templatefinger']) > 0:
                return 'Password'
        else:
            pass

    def daftar(self):
        result = None
        try :
            if self.cek() is False:
                if self.jenisKey() is 'Template' :
                    registering = self.POST (
                        get['SetUserInfoTem'] % (self.name, self.id)
                    )
                    if registering._children:
                        for key_id, key in enumerate(self.key):
                            registering_Template = self.POST (
                                get['SetUserTemplate'] % (
                                    self.id, 
                                    key_id, 
                                    key['size'],
                                    key['valid'],
                                    key['templatefinger']
                                )
                            )
                            if not registering_Template._children :
                                raise AttributeError, registering_Template
                        result = 'Berhasil'
                    else:
                        result = 'Gagal'

                elif self.jenisKey() is 'Password':
                    registering = self.POST (
                        get['SetUserInfoPass'] % (
                            self.name, 
                            self.key[0]['templatefinger'], 
                            self.id)
                    )
                    if registering._children :
                        result = 'Berhasil'
                    else:
                        result = 'Gagal'

            elif self.cek() is True:
                Pegawai.jumlahPegawai -= 1
                result = 'Sudah Terdaftar'
        except Exception:
            result = 'Gagal'
        
        finally:
            if result is 'Gagal' : #rollback
                self.hapus()
                return result
            elif result is 'Berhasil' or result is 'Sudah Terdaftar': #return
                return result
 
    def cek(self):
        whoChecked = self.POST (get['GetUserInfo'] % (self.id))
        try:
            if whoChecked._children :
                return True
            else:
                return False
        except Exception:
            pass
        
    def hapus(self):
        result = False
        try:
            while self.cek() is True:
                whoRemoved = self.POST (get['DeleteUser'] % (self.id))
                if whoRemoved._children:
                    Pegawai.jumlahPegawai -= 1
                    result = True
                else:
                    result = False
        except Exception:
            pass
        finally:
            return result

    def update(self):
        try:
            if self.hapus() :
                if self.daftar() == 'Berhasil':
                    konfirmasi = webAPI.KONFIRM_GANTI_FINGER({
                        "pegawai_id"    : self.id,
                        "ip"            : self.ipAddress,
                        "instansi_id"   : instansi_id.ID_INSTANSI,
                        "status"        : 1,
                        "token"         : encrypt(
                            str(self.id) +
                            str(1) +
                            str(self.ipAddress) +
                            str(instansi_id.ID_INSTANSI)
                        )
                    })
                    return konfirmasi
        except Exception:
            pass
        
class Absensi(metode):
    def __init__ (self, tujuan) :
        metode.__init__(self, tujuan)
        self.mesin              = Mesin(tujuan)
        self.mesin.getMac()
        self.allUser            = 'All'
        self.getAbsensi         = self.POST (get['GetAttLog'] % self.allUser)
        self.jumlahLocal        = dataLocal.cekjumlahabsensi(self.mesin.Mac)
        self.jumlahFinger       = 0
        if self.getAbsensi is not None:
            self.jumlahFinger   = len(self.getAbsensi)

    def ambil(self):
        try:
            if self.getAbsensi._children :
                PIN, TANGGAL, JAM, STATUS = [], [], [], []
                for row in self.getAbsensi.findall('Row'):
                    PIN.append(row.find('PIN').text)
                    TANGGAL.append(row.find('DateTime').text.split()[0])
                    JAM.append(row.find('DateTime').text.split()[1])
                    STATUS.append(row.find('Status').text)

                absensi = [{'PIN'       : pin,
                            'Tanggal'   : tanggal,
                            'Jam'       : jam,
                            'Status'    : status} for pin, tanggal, jam, status in zip (PIN, TANGGAL, JAM, STATUS)]
                hasil = json.loads(json.dumps(absensi))
                return hasil

            else:
                raise AttributeError, self.getAbsensi
        except Exception:
            pass

    def kirim(self):
        dataAbsensi     = self.ambil()
        if self.jumlahFinger > self.jumlahLocal :
            for iterasi in range (self.jumlahLocal, self.jumlahFinger) :
                token   = encrypt(
                    str(dataAbsensi[iterasi]['Jam']) +
                    str(dataAbsensi[iterasi]['Tanggal']) +
                    str(dataAbsensi[iterasi]['PIN']) +
                    str(instansi_id.ID_INSTANSI) +
                    str(dataAbsensi[iterasi]['Status'])
                )

                kirim    = webAPI.KEHADIRAN(
                    {   'status' : dataAbsensi[iterasi]['Status'], 
                        'instansi' : instansi_id.ID_INSTANSI, 
                        'jam' : dataAbsensi[iterasi]['Jam'], 
                        'tanggal' : dataAbsensi[iterasi]['Tanggal'], 
                        'user_id' : dataAbsensi[iterasi]['PIN'], 
                        'token' : token }
                )
                if kirim :
                    dataLocal.inputdataabsensi(
                        dataAbsensi[iterasi]['PIN'], 
                        self.mesin.Mac
                    )
                
                tampil.progress_bar(iterasi, self.jumlahFinger, text='MENGIRIMKAN ABSENSI')
                tampil.disp.image(tampil.image)
                tampil.disp.display()

            tampil.teks(text2='SELESAI')
            time.sleep(1.2)
        else:
            pass

        if self.jumlahFinger > 50000 and self.jumlahLocal > 50000 :
            self.hapus()

    def hapus(self):
        clearAbsensiF   = self.POST(get['ClearData'] % 3)
        try:
            if clearAbsensiF._children :
                dataLocal.hapusdataabsensi(Mesin.Mac)
            else:
                raise AttributeError, clearAbsensiF
        except Exception:
            pass
    
class Mesin(metode):
    Mac = None
    registered      = None
    jumlahPegawai   = None
    jumlahAdmin     = None
    versiSoftware   = None
    jumlahMac       = None
    jumlahAbsensiF  = None
    jumlahAbsensiL  = None
    dataPegawai     = None
    dataAdmin       = None

    def __init__(self, tujuan):
        metode.__init__(self, tujuan)
        self.tujuan             = tujuan
        self.allPegawai         = self.POST (get['GetAllUserInfo'])
        self.getAdmin()
        self.getPegawai()
        self.daftarMac()
        self.getMac()
        Mesin.versiSoftware     = dataLocal.ambilversion()
        Mesin.jumlahMac         = dataLocal.cekjumlahmac()
        self.absensi            = self.POST(get ['GetAttLog'] % 'All')
        if self.absensi is not None :
            Mesin.jumlahAbsensiF = len(self.absensi)
        Mesin.jumlahAbsensiL    = dataLocal.cekjumlahabsensi(Mesin.Mac)
        
    def getMac(self):
        getMac = self.POST (get['GetOption'] % 'MAC')
        try:
            if getMac._children :
                for row in getMac.findall('Row'):
                    Mesin.Mac = row.find('Value').text
                    Mesin.registered = dataLocal.macterdaftar(Mesin.Mac)
            else:
                raise AttributeError, getMac
        except:
            pass

    def getAdmin(self):
        try:
            if self.allPegawai._children :
                Mesin.jumlahAdmin = 0
                for row in self.allPegawai.findall('Row'):
                    if str(row.find('Privilege').text) == str(14):
                        Mesin.jumlahAdmin += 1
            else:
                raise AttributeError, self.allPegawai
        except Exception:
            pass

    def getPegawai(self):
        try:
            if self.allPegawai._children :
                Mesin.jumlahPegawai = 0
                for row in self.allPegawai.findall('Row'):
                    if str(row.find('Privilege').text) == str(0):
                        Mesin.jumlahPegawai += 1
            else:
                raise AttributeError, self.allPegawai
        except Exception:
            pass

    def daftarMac(self):
        macLocal    = dataLocal.cekkesemuamac()
        macAPI      = webAPI.MACADDRESS()
        if macAPI:
            for data_macLocal in macLocal :
                hasil = False
                for data_macAPI in macAPI :
                    if str(data_macLocal[0]) == str(data_macAPI['macaddress']) :
                        hasil = True
                        break
                    else :
                        hasil = False
                if not hasil :
                    dataLocal.hapusmac(data_macLocal[0])
            for data_macAPI in macAPI :
                dataLocal.daftarmac(data_macAPI['macaddress'])

    def semuaPegawai(self):
        hasil = None
        try:
            if self.allPegawai._children :
                Name, Password, Group, Privilege, PIN2 = [], [], [], [], []
                for row in self.allPegawai.findall('Row'):
                    if str(row.find('Privilege').text) == str(0):
                        PIN2.append (row.find('PIN2').text)
                        Name.append (row.find('Name').text)
                        Password.append(row.find('Password').text)
                        Group.append(row.find('Group').text)
                        Privilege.append (row.find('Privilege').text)
                data = [{'PIN' : pin, 'Name' : name, 'Password' : password,'Group' : group, 'Privilege' : privilege} for pin, name, password, group, privilege in zip (PIN2, Name, Password, Group, Privilege)]
                hasil = json.loads(json.dumps(data))
            else:
                hasil = None
        finally:
            return hasil

    def semuaAdmin(self):
        hasil = None
        try:
            if self.allPegawai._children :
                Name, Password, Group, Privilege, PIN2 = [], [], [], [], []
                for row in self.allPegawai.findall('Row'):
                    if str(row.find('Privilege').text) == str(14):
                        PIN2.append (row.find('PIN2').text)
                        Name.append (row.find('Name').text)
                        Password.append(row.find('Password').text)
                        Group.append(row.find('Group').text)
                        Privilege.append (row.find('Privilege').text)
                data = [{'PIN' : pin, 'Name' : name, 'Password' : password,'Group' : group, 'Privilege' : privilege} for pin, name, password, group, privilege in zip (PIN2, Name, Password, Group, Privilege)]
                hasil = json.loads(json.dumps(data))
            else:
                hasil = None
        finally:
            return hasil

    def status(self):
        tulisan = None
        token = encrypt(    str(self.tujuan)+
                            str(Mesin.versiSoftware)+
                            str(Mesin.jumlahMac)+
                            str(Mesin.jumlahPegawai)+
                            str(Mesin.jumlahAdmin)+
                            str(Mesin.jumlahAbsensiF)+
                            str(Mesin.jumlahPegawai)+
                            str(Mesin.jumlahAdmin)+
                            str(Mesin.jumlahAbsensiL)+
                            str(instansi_id.ID_INSTANSI))

        hasil =     webAPI.LOG_RASPBERRY(({ 'ip'                    : self.tujuan,
                                            'versi'                 : Mesin.versiSoftware,
                                            'jumlahmac'             : Mesin.jumlahMac,
                                            'jumlahpegawaifinger'   : Mesin.jumlahPegawai,
                                            'jumlahadminfinger'     : Mesin.jumlahAdmin,
                                            'jumlahabsensifinger'   : Mesin.jumlahAbsensiF,
                                            'jumlahpegawailocal'    : Mesin.jumlahPegawai,
                                            'jumlahadminlocal'      : Mesin.jumlahAdmin,
                                            'jumlahabsensilocal'    : Mesin.jumlahAbsensiL,
                                            'instansi_id'           : instansi_id.ID_INSTANSI,
                                            'token'                 : token
                                        }))
        
        if hasil :
            tulisan = 'CONNECTED'
        else:
            tulisan = 'DISCONNECTED'

        tampil.teks(text1='VERSI : %s' % Mesin.versiSoftware, 
                    text2='JUMLAH PEGAWAI : %s' % Mesin.jumlahPegawai, 
                    text3='STATUS : %s' % tulisan)
        
        
def main_Program(IP_Address):
    try:  
        mesin           = Mesin(IP_Address)
        
        if mesin.registered :
            version         = webAPI.VERSI()
            trigger         = webAPI.TRIGGER()          
            daftar_Pegawai  = webAPI.PEGAWAI()
            daftar_Admin    = webAPI.ADMIN()
            update_Pegawai  = webAPI.GANTI_FINGER(IP_Address)
            absensi         = Absensi(IP_Address)

            absensi.kirim()
            mesin.status()

            if trigger is 1:
                if update_Pegawai is not None :
                    for pegawai in update_Pegawai :
                        oPegawai = Pegawai( IP_Address,pegawai['pegawai_id'],pegawai['nama'])
                        oPegawai.update()

                if (daftar_Admin and daftar_Pegawai) is not None:
                    if len(daftar_Admin) != mesin.jumlahAdmin : #Admin
                        if mesin.semuaAdmin() is not None:
                            for adminFinger in mesin.semuaAdmin():
                                hasil = False
                                for adminAPI in daftar_Admin:
                                    if str(adminAPI['pegawai_id']) == str(adminFinger['PIN']):
                                        hasil = True
                                        break
                                    else:
                                        hasil =False
                                if not hasil:
                                    oAdmin = Admin(IP_Address, adminFinger['PIN'], adminFinger['Name'])
                                    oAdmin.hapus()
                            for admin in daftar_Admin:
                                oAdmin = Admin(IP_Address, admin['id'], admin['nama'])
                                oAdmin.daftar()
                        else:
                            for admin in daftar_Admin:
                                oAdmin = Admin(IP_Address, admin['id'], admin['nama'])
                                oAdmin.daftar()
                    
                    if len(daftar_Pegawai) != mesin.jumlahPegawai : #Pegawai
                        if mesin.semuaPegawai() is not None:
                            for pegawaiFinger in mesin.semuaPegawai():
                                hasil = False
                                for pegawaiAPI in daftar_Pegawai:
                                    if str(pegawaiAPI['pegawai_id']) == str(pegawaiFinger['PIN']):
                                        hasil = True
                                        break
                                    else:
                                        hasil =False
                                if not hasil:
                                    oPegawai = Pegawai(IP_Address, pegawaiFinger['PIN'], pegawaiFinger['Name'])
                                    oPegawai.hapus()
                            for loading, pegawai in enumerate(daftar_Pegawai):
                                oPegawai = Pegawai(IP_Address, pegawai['id'], pegawai['nama'])
                                oPegawai.daftar()

                                tampil.progress_bar(loading+1, len(daftar_Pegawai), text='MENAMBAHKAN PEGAWAI')
                                tampil.disp.image(tampil.image)
                                tampil.disp.display()
                        else:
                            for loading, pegawai in enumerate(daftar_Pegawai):
                                oPegawai = Pegawai(IP_Address, pegawai['id'], pegawai['nama'])
                                oPegawai.daftar()

                                tampil.progress_bar(loading+1, len(daftar_Pegawai), text='MENAMBAHKAN PEGAWAI')
                                tampil.disp.image(tampil.image)
                                tampil.disp.display()

            elif trigger is 3:
                if dataLocal.cekversion(version) :
                    update(version)
                else:
                    raise Exception
    
        else:
            tampil.teks(text1='MACADDRESS',text2='FINGERPRINT',text3='BELUM TERDAFTAR')
            time.sleep(1.2)
            tampil.teks(text1='SILAKAN',text2='HUBUNGI PIHAK',text3='DISKOMINFO')
            time.sleep(1.2)

    except Exception:
        logger.error(Exception)
        tampil.teks(text1='ERROR',text2='RESTART',text3='RASPBERRY')
        run('sudo reboot', shell=True)
        

# for pegawai in update_Pegawai:
#     oPegawai = Pegawai('10.10.10.10',pegawai['pegawai_id'], pegawai['nama'])
#     print "Pendaftaran {}, {}".format(oPegawai.name, oPegawai.update())
# print "Total Pegawai Berhasil Di Daftarkan: {}".format(Pegawai.jumlahPegawai)


# if __name__ == "__main__" :
#     while True:
#         main_Program('10.10.10.10')

# print encrypt("10219110.10.10.1019")

#Yang Belum
#Konfirmasi Update Pegawai
#Update
#Main

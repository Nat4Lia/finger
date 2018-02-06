import xml.etree.ElementTree as ET
import FingerCommandLib as FingerCommand
import Web_Access as Server


def parsingFromFinger(data):
    try :
        # print data
        parsed = ET.fromstring(data)
        return parsed
    except ET.ParseError as err :
        pass
    except IndexError as err:
        pass
    except ValueError as err:
        pass
    except TypeError as err:
        pass

#Fungsi Hapus Semua
def hapussemua (tujuan, alamat):
    hapus = FingerCommand.fingerprint(tujuan, alamat).ClearData(1)
    return hapus

#Fungsi Ambil Data MAC
def ambilmacaddress(tujuan, alamat):
    while True:
        try:
            alamatmac   = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).Option('MAC'))[0][0].text
            return alamatmac
        except TypeError as err:
            pass
        except ValueError as err:
            pass
        except IndexError as err:
            pass

#Fungsi Cek Jumlah Pegawai
def jumlahpegawai(tujuan, alamat):
    try:
        banyakpegawai = len(parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).GetAllUserInfo()))
        return banyakpegawai
    except TypeError as err:
        pass
    except ValueError as err:
        pass
    except IndexError as err:
        pass

# Fungsi Cek Pegawai Finger
def cekpegawai(tujuan, alamat, pegawaiid):
    try:
        cekUserFinger = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).GetUserInfo(pegawaiid))
        if len(cekUserFinger) == 0:
            return False
        elif len(cekUserFinger) == 1:
            while True:
                try :
                    if str(pegawaiid) == str(cekUserFinger[0][6].text):
                        return True
                    else :
                        return False
                except TypeError as err:
                    pass
                except IndexError as err:
                    pass
    except TypeError as err:
        pass

#Fungsi Hapus Pegawai Finger
def hapuspegawai(tujuan, alamat, pegawaiid):
    try:
        while True:
            if cekpegawai(tujuan, alamat, pegawaiid) :
                hapus = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).DeleteUser(pegawaiid))[0][1].text
            else:
                return True
    except TypeError as err:
        pass
        return False
    except ValueError as err:
        pass
        return False
    except IndexError as err:
        pass
        return False

#Fungsi Daftar Pegawai
def daftarpegawai(tujuan, alamat, pegawaiid, nama):
    if not cekpegawai(tujuan, alamat, pegawaiid):
        loadtemplate = Server.load('Template', pegawaiid)
        while True:
            try:
                statusdaftaruser = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).SetUserInfo(nama, pegawaiid))[0][1].text
                if statusdaftaruser == 'Successfully!':
                    statusSetTemplate = [None,None]
                    for template in range (0, len(loadtemplate)):
                        size            = loadtemplate[template]['size']
                        valid           = loadtemplate[template]['valid']
                        finger_template = loadtemplate[template]['templatefinger']
                        try:
                            statusSetTemplate[template] = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).SetUserTemplate(pegawaiid, template, size, valid, finger_template))[0][1].text
                        except TypeError as err:
                            pass
                        except ValueError as err:
                            pass
                        except IndexError as err:
                            pass
                    # print statusSetTemplate[0], statusSetTemplate[1]
                    if (statusSetTemplate[0] == 'Successfully!') and (statusSetTemplate[1] == 'Successfully!'):
                        return True
                    else:
                        hapuspegawai(tujuan, alamat, pegawaiid)
                else:
                    hapuspegawai(tujuan, alamat, pegawaiid)
            except TypeError as err:
                hapuspegawai(tujuan, alamat, pegawaiid)
                pass
            except ValueError as err:
                hapuspegawai(tujuan, alamat, pegawaiid)
                pass
            except IndexError as err:
                hapuspegawai(tujuan, alamat, pegawaiid)
                pass
    else:
        return False

#Fungsi Daftar Admin
def daftaradmin(tujuan, alamat, pegawaiid, nama):
    if not cekpegawai(tujuan, alamat, pegawaiid):
        loadtemplate = Server.load('Template', pegawaiid)
        while True:
            try:
                statusdaftaruser = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).SetAdminUser(nama, pegawaiid))[0][1].text
                if statusdaftaruser == 'Successfully!':
                    statusSetTemplate = [None,None]
                    for template in range (0, len(loadtemplate)):
                        size            = loadtemplate[template]['size']
                        valid           = loadtemplate[template]['valid']
                        finger_template = loadtemplate[template]['templatefinger']
                        try:
                            statusSetTemplate[template] = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).SetUserTemplate(pegawaiid, template, size, valid, finger_template))[0][1].text
                        except TypeError as err:
                            pass
                        except ValueError as err:
                            pass
                        except IndexError as err:
                            pass
                    if (statusSetTemplate[0] == 'Successfully!') and (statusSetTemplate[1] == 'Successfully!'):
                        return True
                    else:
                        hapuspegawai(tujuan, alamat, pegawaiid)
                else:
                    hapuspegawai(tujuan, alamat, pegawaiid)
            except TypeError as err:
                hapuspegawai(tujuan, alamat, pegawaiid)
                pass
            except ValueError as err:
                hapuspegawai(tujuan, alamat, pegawaiid)
                pass
            except IndexError as err:
                hapuspegawai(tujuan, alamat, pegawaiid)
                pass
    else:
        return False

#Fungsi Hapus Data Absensi
def hapusabsensi(tujuan, alamat):
    hapus = FingerCommand.fingerprint(tujuan, alamat).ClearData(3)
    return hapus

#Fungsi Mengambil Data Absensi
def ambildataabsensi(tujuan, alamat):
    while True:
        try:
            absensi = parsingFromFinger(FingerCommand.fingerprint(tujuan,alamat).GetAttLog('All'))
            return absensi
        except TypeError as err:
            pass
        except ValueError as err:
            pass

#Fungsi Mengambil semua data pegawai
def semuadatapegawai(tujuan, alamat):
    try:
        semuapegawai = parsingFromFinger(FingerCommand.fingerprint(tujuan, alamat).GetAllUserInfo())
        return semuapegawai
    except TypeError as err:
        pass
    except ValueError as err:
        pass

# print daftarpegawai('Finger A','10.10.10.10:80',15,'FAHRUL')
# print cekpegawai('Finger A','10.10.10.10:80',15)
# hapuspegawai('Finger', '10.10.10.10:80', 15)
# print jumlahpegawai('Finger', '10.10.10.10:80')
# print semuadatapegawai('Finger', '10.10.10.10:80')[0][4].text
# print hapussemua('Finger A','10.10.10.10')

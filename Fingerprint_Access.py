import xml.etree.ElementTree as ET
import getDataFinger as FingerCommand
import Web_Access as Server


def parsingFromFinger(data):
    try :
        # print data
        parsed = ET.fromstring(data)
        return parsed
    except ET.ParseError as err :
        print err
    except IndexError as err:
        print err
    except ValueError as err:
        print err
    except TypeError as err:
        print err

#Fungsi Hapus Semua
def hapussemua (tujuan, alamat):
    hapus = FingerCommand.clearData(tujuan, alamat, 0, 1).get()
    return hapus

#Fungsi Ambil Data MAC
def ambilmacaddress(tujuan, alamat):
    while True:
        try:
            alamatmac   = parsingFromFinger(FingerCommand.getOption(tujuan, alamat, 0, 'MAC').get())[0][0].text
            return alamatmac
        except TypeError as err:
            print err
        except ValueError as err:
            print err
        except IndexError as err:
            print err

#Fungsi Cek Jumlah Pegawai
def jumlahpegawai(tujuan, alamat):
    try:
        banyakpegawai = len(parsingFromFinger(FingerCommand.getAllUserInfo(tujuan, alamat, 0).get()))
        return banyakpegawai
    except TypeError as err:
        print err
    except ValueError as err:
        print err
    except IndexError as err:
        print err

#Fungsi Hapus Pegawai Finger
def hapuspegawai(tujuan, alamat, pegawaiid):
    try:
        hapus = parsingFromFinger(FingerCommand.delUser(tujuan, alamat, 0, pegawaiid).delete())[0][1].text
        if hapus == 'Successfully!':
            return True
        else:
            return False
    except TypeError as err:
        print err
        return False
    except ValueError as err:
        print err
        return False
    except IndexError as err:
        print err
        return False

# Fungsi Cek Pegawai Finger
def cekpegawai(tujuan, alamat, pegawaiid):
    try:
        cekUserFinger = parsingFromFinger(FingerCommand.getUserInfo(tujuan, alamat, 0, pegawaiid).get())
        if len(cekUserFinger) == 0:
            return False
        elif len(cekUserFinger) == 1:
            while True:
                try :
                    if str(pegawaiid) == cekUserFinger[0][6].text:
                        return True
                    else :
                        return False
                except TypeError as err:
                    print err
                except IndexError as err:
                    print err
    except TypeError as err:
        print err

#Fungsi Daftar Pegawai
def daftarpegawai(tujuan, alamat, pegawaiid, nama):
    if not cekpegawai(tujuan, alamat, pegawaiid):
        loadtemplate = Server.load('Template', pegawaiid)
        while True:
            try:
                statusdaftaruser = parsingFromFinger(FingerCommand.setUserInfo(tujuan, alamat, 0, nama, pegawaiid).get())[0][1].text
                if statusdaftaruser == 'Successfully!':
                    statusSetTemplate = [None,None]
                    for template in range (0, len(loadtemplate)):
                        size            = loadtemplate[template]['size']
                        valid           = loadtemplate[template]['valid']
                        finger_template = loadtemplate[template]['templatefinger']
                        try:
                            statusSetTemplate[template] = parsingFromFinger(FingerCommand.setUserTemplate(tujuan, alamat, 0, pegawaiid, template, size, valid, finger_template).get())[0][1].text
                        except TypeError as err:
                            print err
                        except ValueError as err:
                            print err
                        except IndexError as err:
                            print err
                    if (statusSetTemplate[0] == 'Successfully!') and (statusSetTemplate[1] == 'Successfully!'):
                        return True
                    else:
                        hapuspegawai(tujuan, alamat, pegawaiid)
                else:
                    hapuspegawai(tujuan, alamat, pegawaiid)
            except TypeError as err:
                print err
                hapuspegawai(tujuan, alamat, pegawaiid)
            except ValueError as err:
                print err
                hapuspegawai(tujuan, alamat, pegawaiid)
            except IndexError as err:
                print err
                hapuspegawai(tujuan, alamat, pegawaiid)
    else:
        return False

#Fungsi Daftar Admin
def daftaradmin(tujuan, alamat, pegawaiid, nama):
    if not cekpegawai(tujuan, alamat, pegawaiid):
        print 'Mendaftarkan %s' % nama
        loadtemplate = Server.load('Template', pegawaiid)
        while True:
            try:
                statusdaftaruser = parsingFromFinger(FingerCommand.setAdminUser(tujuan, alamat, 0, nama, pegawaiid).get())[0][1].text
                if statusdaftaruser == 'Successfully!':
                    statusSetTemplate = [None,None]
                    for template in range (0, len(loadtemplate)):
                        size            = loadtemplate[template]['size']
                        valid           = loadtemplate[template]['valid']
                        finger_template = loadtemplate[template]['templatefinger']
                        print 'Mendaftarkan Template...'
                        try:
                            statusSetTemplate[template] = parsingFromFinger(FingerCommand.setUserTemplate(tujuan, alamat, 0, pegawaiid, template, size, valid, finger_template).get())[0][1].text
                        except TypeError as err:
                            print err
                        except ValueError as err:
                            print err
                        except IndexError as err:
                            print err
                    if (statusSetTemplate[0] == 'Successfully!') and (statusSetTemplate[1] == 'Successfully!'):
                        return True
                    else:
                        hapuspegawai(tujuan, alamat, pegawaiid)
                else:
                    hapuspegawai(tujuan, alamat, pegawaiid)
            except TypeError as err:
                print err
                hapuspegawai(tujuan, alamat, pegawaiid)
            except ValueError as err:
                print err
                hapuspegawai(tujuan, alamat, pegawaiid)
            except IndexError as err:
                print err
                hapuspegawai(tujuan, alamat, pegawaiid)
    else:
        return False

#Fungsi Hapus Data Absensi
def hapusabsensi(tujuan, alamat):
    hapus = FingerCommand.clearData(tujuan, alamat, 0, 3).get()
    return hapus

#Fungsi Mengambil Data Absensi
def ambildataabsensi(tujuan, alamat):
    while True:
        try:
            absensi = parsingFromFinger(FingerCommand.getAttLog(tujuan,alamat,0,'All').get())
            return absensi
        except TypeError as err:
            print err
        except ValueError as err:
            print err

# print daftarpegawai('Finger A','10.10.10.10:80',15,'FAHRUL')
# print cekpegawai('Finger A','10.10.10.10:80',15)
# hapuspegawai('Finger', '10.10.10.10:80', 15)
# print jumlahpegawai('Finger', '10.10.10.10:80')
# print ambilmacaddress('Finger', '10.10.10.10:80')

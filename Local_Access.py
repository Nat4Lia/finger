import mysql.connector

config = {
	'user': 'root',
	'password': 'eabsen.kalselprov.go.id',
	'host': 'localhost',
	'database': 'data_finger',
	'raise_on_warnings': True,

}

#TEST ACCOUNT
# config = {
# 	'user': 'root',
# 	'password': '123456',
# 	'host': 'localhost',
# 	'database': 'data_finger',
# 	'raise_on_warnings': True,

# }


SQL_SYNTAX = {
                'ADDPEGAWAI' 	      : 'INSERT INTO pegawai (user_pin2, user_name, mac_) VALUES (%s, %s, %s)',
                'ADDADMIN' 		      : 'INSERT INTO pegawaiAdmin (user_pin2, user_name, mac_) VALUES (%s, %s, %s)',
                'ADDMAC'		      : 'INSERT INTO macaddress (mac_) VALUES (%s)',
                'ADDATTENDANCE'	      : 'INSERT INTO attendance (user_pin, mac_) VALUES (%s, %s)',
                'ADDVERSION'          : 'INSERT INTO version (version) VALUES (%s)',
                'CHECKATTENDANCE'     : 'SELECT COUNT(*) FROM attendance WHERE mac_ = (%s)',
                'CHECKPEGAWAI'	      : 'SELECT COUNT(*) FROM pegawai WHERE mac_ = (%s)',
                'CHECKADMIN'	      : 'SELECT COUNT(*) FROM pegawaiAdmin WHERE mac_ = (%s)',
                'CHECKMAC'		      : 'SELECT COUNT(*) FROM macaddress',
                'CHECKALLATTENDANCE'  : 'SELECT COUNT(*) FROM attendance',
                'CHECKALLADMIN'       : 'SELECT COUNT(*) FROM pegawaiAdmin',
                'CHECKALLPEGAWAI'     : 'SELECT COUNT(*) FROM pegawai',
                'CHECKVERSION'        : 'SELECT version FROM version',
                'DELETEMAC'	      	  : 'DELETE FROM macaddress WHERE mac_ = (%s)',
                'DELETEPEGAWAI'	      : 'DELETE FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'DELETEPEGAWAIID'	  : 'DELETE FROM pegawai WHERE id = (%s) AND mac_ = (%s)',
                'DELETEADMIN'	      : 'DELETE FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'DELETEADMINID'	      : 'DELETE FROM pegawaiAdmin WHERE id = (%s) AND mac_ = (%s)',
                'DELETEATTENDANCE'    : 'DELETE FROM attendance WHERE mac_ = (%s)',
                'FINDMAC'		      : 'SELECT mac_ FROM macaddress WHERE mac_ = (%s)',
                'FINDALLMAC'          : 'SELECT mac_ FROM macaddress',
                'FINDALLADMIN'	      : 'SELECT user_pin2 FROM pegawaiAdmin WHERE mac_ = (%s)',
                'FINDADMIN'		      : 'SELECT user_pin2 FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDPEGAWAI'	      : 'SELECT user_pin2 FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDPEGAWAIALL'      : 'SELECT * FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDADMINALL'        : 'SELECT * FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDALLPEGAWAI'      : 'SELECT user_pin2 FROM pegawai WHERE mac_ = (%s)',
                'UPDATEVERSION'       : 'UPDATE version SET version = %s',
                'TRUNCATE'		      : 'TRUNCATE TABLE attendance'
}

class Localhost:
    def __init__ (self):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor(buffered=True)
        self.cnx.commit()

    def hapussemua(self):
        self.cursor.execute('TRUNCATE TABLE attendance')
        self.cursor.execute('TRUNCATE TABLE macaddress')
        self.cursor.execute('TRUNCATE TABLE pegawai')
        self.cursor.execute('TRUNCATE TABLE pegawaiAdmin')
        self.cnx.commit()
        if self.ceksemuaabsensi() is 0 and self.ceksemuaadmin() is 0 and self.ceksemuapegawai() is 0 and self.cekjumlahmac() is 0 :
            return True
        else:
            return False

    def cekversion(self, version):
        self.cursor.execute(SQL_SYNTAX['CHECKVERSION'])
        try:
            versionsekarang = self.cursor.fetchone()[0]
            if versionsekarang == version:
                return False
            else:
                return True
        except TypeError as err:
            return True

    def ambilversion(self):
        self.cursor.execute(SQL_SYNTAX['CHECKVERSION'])
        try:
            versionsekarang = self.cursor.fetchone()[0]
            return versionsekarang
        except IndexError as err:
            pass
        except TypeError as err:
            pass

    def updateversion(self, version):
        self.cursor.execute(SQL_SYNTAX['UPDATEVERSION'], (version,))
        self.cnx.commit()

    def tambahversion(self, version):
        self.cursor.execute(SQL_SYNTAX['ADDVERSION'], (version,))
        self.cnx.commit()

#MacAddress

    def hapusmac(self, mac):
        self.cursor.execute(SQL_SYNTAX['DELETEMAC'], (mac,))
        self.cnx.commit()

    def cekkesemuamac(self):
        self.cursor.execute(SQL_SYNTAX['FINDALLMAC'])
        data = self.cursor.fetchall()
        return data

    def macterdaftar(self, mac):
        self.cursor.execute(SQL_SYNTAX['FINDMAC'], (mac,))
        try:
            macterdaftar = self.cursor.fetchone()[0]
            if macterdaftar == mac:
                return True
            else :
                return False
        except TypeError as err:
            return False
        except IndexError as err:
            return False
            
    def daftarmac(self, mac):
        if not self.macterdaftar(mac) :
            self.cursor.execute(SQL_SYNTAX['ADDMAC'], (mac,))
            self.cnx.commit()
            return True
        else:
            return False

    def cekjumlahmac(self):
        self.cursor.execute(SQL_SYNTAX['CHECKMAC'])
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass
        except IndexError as err:
            pass
        except ValueError as err:
            pass

#Pegawai
    def ceksemuapegawai(self):
        self.cursor.execute(SQL_SYNTAX['CHECKALLPEGAWAI'])
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass

    def cekjumlahpegawai(self, mac):
        self.cursor.execute(SQL_SYNTAX['CHECKPEGAWAI'], (mac,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass

    def cekpegawai (self, pegawaiid, mac):
        self.cursor.execute(SQL_SYNTAX['FINDPEGAWAI'], (pegawaiid, mac,))
        try:
            pegawai = self.cursor.fetchone()
            if str(pegawai[0]) == str(pegawaiid):
                return True
            else:
                return False
        except TypeError as err:
            return False

    def carisemuapegawai(self, mac):
        self.cursor.execute(SQL_SYNTAX['FINDALLPEGAWAI'], (mac,))
        data    = self.cursor.fetchall()
        return data

    def hapuspegawai(self, pegawaiid, mac):
        self.cursor.execute(SQL_SYNTAX['DELETEPEGAWAI'], (pegawaiid, mac,))
        self.cnx.commit()
        if not Localhost().cekpegawai(pegawaiid, mac):
            return True
        else:
            return False

    def hapuspegawaiid(self, idlocal, mac):
        self.cursor.execute(SQL_SYNTAX['DELETEPEGAWAIID'], (idlocal, mac,))
        self.cnx.commit()

    def normalizelocalhostpegawai (self, pegawaiid, mac) :
        self.cursor.execute(SQL_SYNTAX['FINDPEGAWAIALL'], (pegawaiid, mac,))
        data    = self.cursor.fetchall()
        return data

    def daftarpegawai(self, pegawaiid, nama, mac):
        while True:
            if not Localhost().cekpegawai(pegawaiid, mac): #Cek Pegawai Jika Sudah Ada Maka Tidak Didaftarkan
                self.cursor.execute(SQL_SYNTAX['ADDPEGAWAI'], (pegawaiid, nama, mac,))
                self.cnx.commit()
                if Localhost().cekpegawai(pegawaiid, mac):
                    return True
                else:
                    return False
            else:
                return False


#admin
    def ceksemuaadmin(self):
        self.cursor.execute(SQL_SYNTAX['CHECKALLADMIN'])
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass

    def cekjumlahadmin(self, mac):
        self.cursor.execute(SQL_SYNTAX['CHECKADMIN'], (mac,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass

    def cekadmin (self, pegawaiid, mac):
        self.cursor.execute(SQL_SYNTAX['FINDADMIN'], (pegawaiid, mac,))
        try:
            admin = self.cursor.fetchone()
            if str(admin[0]) == str(pegawaiid):
                return True
            else:
                return False
        except TypeError as err:
            return False

    def hapusadmin(self, pegawaiid, mac):
        self.cursor.execute(SQL_SYNTAX['DELETEADMIN'], (pegawaiid, mac,))
        self.cnx.commit()
        if not Localhost().cekpegawai(pegawaiid, mac):
            return True
        else:
            return False

    def hapusadminid(self, idlocal, mac):
        self.cursor.execute(SQL_SYNTAX['DELETEADMINID'], (idlocal, mac,))
        self.cnx.commit()

    def normalizelocalhostadmin (self, pegawaiid, mac) :
        self.cursor.execute(SQL_SYNTAX['FINDADMINALL'], (pegawaiid, mac,))
        data    = self.cursor.fetchall()
        return data

    def daftaradmin(self, pegawaiid, nama, mac):
        while True:
            if not Localhost().cekadmin(pegawaiid, mac): #Cek Pegawai Jika Sudah Ada Maka Tidak Didaftarkan
                self.cursor.execute(SQL_SYNTAX['ADDADMIN'], (pegawaiid, nama, mac,))
                self.cnx.commit()
                return True
            else:
                return False

    def carisemuaadmin(self, mac):
        self.cursor.execute(SQL_SYNTAX['FINDALLADMIN'], (mac,))
        data    = self.cursor.fetchall()
        return data

#Data Absensi
    def ceksemuaabsensi(self):
        self.cursor.execute(SQL_SYNTAX['CHECKALLATTENDANCE'])
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass
        except IndexError as err:
            pass

    def cekjumlahabsensi(self, mac):
        self.cursor.execute(SQL_SYNTAX['CHECKATTENDANCE'], (mac,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError as err:
            pass
        except IndexError as err:
            pass

    def inputdataabsensi(self, pegawaiid, mac):
        self.cursor.execute(SQL_SYNTAX['ADDATTENDANCE'], (pegawaiid, mac,))
        self.cnx.commit()

    def cleardataabsensi(self):
        self.cursor.execute(SQL_SYNTAX['TRUNCATE'])
        self.cnx.commit()

    def hapusdataabsensi(self, mac):
        self.cursor.execute(SQL_SYNTAX['DELETEATTENDANCE'], (mac,))
        self.cnx.commit()

# print Localhost().daftarpegawai(1, 'qwerty', '00:17:61:11:6A:C2')
# print Localhost().cekjumlahmac()
# for x in range (0, 1500):
#     print Localhost().normalizelocalhost(x,'00:17:61:11:6A:C2')
# print Localhost().cekkesemuamac('00:17:61:11:6a:c3')
# print Localhost().hapussemua()

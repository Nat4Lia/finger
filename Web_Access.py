import time
import requests
import json
import socket
import lcd_ as cetak

URL = {
		'KEHADIRAN'           : 'http://eabsen.kalselprov.go.id/api/attendance',
		'AMBILTEMPLATE'       : 'http://eabsen.kalselprov.go.id/api/ambilfinger/%s',
		'TRIGGER'             : 'http://eabsen.kalselprov.go.id/api/triger',
		'CEKPEGAWAI'          : 'http://eabsen.kalselprov.go.id/api/cekpegawai/%s',
		'CEKADMIN'            : 'http://eabsen.kalselprov.go.id/api/admin/finger',
		'AMBILMAC'            : 'http://eabsen.kalselprov.go.id/api/macaddress',
		'CEKIDPEGAWAI'        : 'http://eabsen.kalselprov.go.id/api/cekpegawaidata/%s',
		'CEKIDADMIN'          : 'http://eabsen.kalselprov.go.id/api/admin/finger/%s',
        'CEKVERSI'            : 'http://eabsen.kalselprov.go.id/api/version',
        'LOGERRORUSER'        : 'http://eabsen.kalselprov.go.id/api/logerror',
        'HAPUSPEGAWAI'        : 'http://eabsen.kalselprov.go.id/api/hapusfingerpegawai',
        'LOGRASPBERRY'        : 'http://eabsen.kalselprov.go.id/api/lograspberry'
}

#
# URL = {
# 		'KEHADIRAN'           : 'http://192.168.113.56/api/attendance',
# 		'AMBILTEMPLATE'       : 'http://192.168.113.56/api/ambilfinger/%s',
# 		'TRIGGER'             : 'http://192.168.113.56/api/triger',
# 		'CEKPEGAWAI'          : 'http://192.168.113.56/api/cekpegawai/%s',
# 		'CEKADMIN'            : 'http://192.168.113.56/api/admin/finger',
# 		'AMBILMAC'            : 'http://192.168.113.56/api/macaddress',
# 		'CEKIDPEGAWAI'        : 'http://192.168.113.56/api/cekpegawaidata/%s',
# 		'CEKIDADMIN'          : 'http://192.168.113.56/api/admin/finger/%s',
#         'CEKVERSI'            : 'http://192.168.113.56/api/version',
#         'LOGERRORUSER'        : 'http://192.168.113.56/api/logerror',
#         'HAPUSPEGAWAI'        : 'http://192.168.113.56/api/hapusfingerpegawai',
#         'LOGRASPBERRY'        : 'http://192.168.113.56/api/lograspberry'
# }


# Fungsi{

# Fungsi post
def POST (indeks, header, payload) :
    while True:
        coba = 0
        try:
            r = requests.post(URL[indeks], headers=header, json=payload)
            if r.status_code is 200:
                return True
        except requests.exceptions.RequestException as err:
            cetak.printLCD('Gagal Mengirim','Data Ke Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.Timeout as err:
            cetak.printLCD('Gagal Mengirim','Data Ke Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.ConnectionError as err:
            cetak.printLCD('Gagal Mengirim','Data Ke Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.HTTPError as err:
            cetak.printLCD('Gagal Mengirim','Data Ke Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.ConnectTimeout as err:
            cetak.printLCD('Gagal Mengirim','Data Ke Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()

# Fungsi get
def GET (URL) :
    while True:
        coba = 0
        try:
            r = requests.get(URL, timeout=5)
            if r.status_code is 200:
                return r
        except requests.exceptions.RequestException as err:
            cetak.printLCD('Gagal Mengambil','Data Dari Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.Timeout as err:
            cetak.printLCD('Gagal Mengambil','Data Dari Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.ConnectionError as err:
            cetak.printLCD('Gagal Mengambil','Data Dari Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.HTTPError as err:
            cetak.printLCD('Gagal Mengambil','Data Dari Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()
        except requests.exceptions.ConnectTimeout as err:
            cetak.printLCD('Gagal Mengambil','Data Dari Server').lcd_status()
            cetak.printLCD('Mencoba Lagi','...').lcd_status()
            cetak.printLCD('Mohon Tunggu','...').lcd_status()

# Fungsi Parsing Json
def loadJSON(data):
    try:
        JSONloaded = json.loads(data.content)
        return JSONloaded
    except ValueError as err:
        pass
    except IndexError as err:
        pass
    except TypeError as err:
        pass
    except Exception as err:
        pass

#Fungsi Cek
def load(data, parameter):
    option = { 'Trigger'        : loadJSON(GET(URL['TRIGGER']))[0]['status'],
               'Pegawai'        : loadJSON(GET(URL['CEKPEGAWAI'] % parameter)),
               'Template'       : loadJSON(GET(URL['AMBILTEMPLATE'] % parameter)),
               'Admin'          : loadJSON(GET(URL['CEKADMIN'])),
               'Update'         : loadJSON(GET(URL['CEKVERSI']))['version'],
               'CekPegawai'     : loadJSON(GET(URL['CEKIDPEGAWAI'] % parameter)),
               'CekAdmin'       : loadJSON(GET(URL['CEKIDADMIN'] % parameter)),
               'Macaddress'     : loadJSON(GET(URL['AMBILMAC'])),
               'HapusPegawai'   : loadJSON(GET(URL['HAPUSPEGAWAI']))
    }

    while True:
        try:
            hasil = option[data]
            return hasil
        except TypeError as err:
            pass
# }

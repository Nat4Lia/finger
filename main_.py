import lcd_
import time

listAlamat = {
                'fingerA' : 'http://10.10.10.10:80',
                'fingerB' : 'http://10.10.10.20:80',
                'fingerC' : 'http://10.10.10.30:80',
                'fingerD' : 'http://10.10.10.40:80',
                'fingerE' : 'http://10.10.10.50:80'
}

useAlamat = {}

def checkAlamat() :
    for alamat in listAlamat :
        if check_connection.onCheck(alamat, listAlamat[alamat], 5).checkAlamat() :
            listAlamat[alamat] = listAlamat[alamat].replace("http://","")
            useAlamat[alamat] = listAlamat[alamat]
            print 'Alamat %s Valid' % alamat
        else :
            lcd_.printLCD ('Alamat %s' % alamat, 'Tidak Valid').lcd_status()
            print 'Alamat %s Tidak Valid' % alamat
    print useAlamat

lcd_.printLCD('Starting','%c %c %c' % (32, 32, 32)).lcd_status()
time.sleep(3)
lcd_.printLCD('Starting','%c %c %c' % (46, 32, 32)).lcd_status()
time.sleep(4)
lcd_.printLCD('Starting','%c %c %c' % (46, 46, 32)).lcd_status()
time.sleep(5)
lcd_.printLCD('Starting','%c %c %c' % (46, 46, 46)).lcd_status()

import check_connection
import getDataFinger
import database_
checkAlamat()
while True:
    database_.addMacToLocalHost()
    database_.clone()
    for alamat in useAlamat :
        teks = alamat
        URL = useAlamat[alamat]
        proses = database_.proses(alamat, URL)
        proses.sendLogToServer()
        proses.setUser()
        proses.setAdmin()
        proses.clearLog()

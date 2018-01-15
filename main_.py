import lcd_
import database_baru
import Fingerprint_Access as Finger
import time

listAlamat = {
                'Finger A' : 'http://10.10.10.10:80',
                'Finger B' : 'http://10.10.10.20:80',
                'Finger C' : 'http://10.10.10.30:80',
                'Finger D' : 'http://10.10.10.40:80',
                'Finger E' : 'http://10.10.10.50:80'
}

useAlamat = {}

def checkAlamat() :
    for alamat in listAlamat :
        if check_connection.onCheck(alamat, listAlamat[alamat], 5).checkAlamat() :
            listAlamat[alamat] = listAlamat[alamat].replace("http://","")
            useAlamat[alamat] = listAlamat[alamat]
        else :
            pass


lcd_.printLCD('Starting v2.1','%c %c %c' % (32, 32, 32)).lcd_status()
time.sleep(3)
lcd_.printLCD('Starting v2.1','%c %c %c' % (46, 32, 32)).lcd_status()
time.sleep(4)
lcd_.printLCD('Starting v2.1','%c %c %c' % (46, 46, 32)).lcd_status()
time.sleep(5)
lcd_.printLCD('Starting v2.1','%c %c %c' % (46, 46, 46)).lcd_status()


import check_connection
checkAlamat()
if len(useAlamat) is 0 :
    lcd_.printLCD ('Tidak Ada Fingerprint', 'Yang Terhubung').lcd_status()
    time.sleep(10)
    lcd_.printLCD ('Harap Hubungkan', 'Raspberry ke Fingerprint').lcd_status()
    time.sleep(10)
    lcd_.printLCD ('Kemudian Restart', 'Raspberry').lcd_status()
    time.sleep(10)

else:
    lcd_.printLCD ('Raspberry Ini', 'Menggunakan').lcd_status()
    lcd_.printLCD ('%s Buah' % len(useAlamat), 'Fingerprint').lcd_status()
    database_baru.resetall(useAlamat)
    while True:
        database_baru.clone()
        database_baru.resetall(useAlamat)
        database_baru.daftarmac()
        for alamat in useAlamat :
            teks = alamat
            URL = useAlamat[alamat]
            proses = database_baru.Proses(alamat, URL)
            proses.kirimdataabsensi()
            proses.clearlog()
            proses.manajemenadmin()
            proses.manajemenuser()
            proses.kirimstatus()

import lcd_ as tampil
import Fingerprint
import time
from check_connection import connection_on as connect
import Local_Access
localhost = Local_Access.Localhost()

listAlamat = ['10.10.10.10',
              '10.10.10.20',
              '10.10.10.30',
              '10.10.10.40',
              '10.10.10.50']

useAlamat = []
def checkAlamat() :
    for i,alamat in enumerate(listAlamat) :
        tampil.progress_bar(i+1, len(listAlamat), text='%s' % localhost.ambilversion())
        tampil.disp.image(tampil.image)
        tampil.disp.display()
        if connect(alamat) :
            useAlamat.append(alamat)

if __name__ == "__main__" :
    checkAlamat()
    if len(useAlamat) is 0 :
        while True:
            tampil.teks(text1='TIDAK ADA',text2='FINGERPRINT',text3='YANG TERHUBUNG')
            time.sleep(1.2)
            tampil.teks(text1='HARAP HUBUNGKAN',text2='RASPBERRY',text3='KE FINGERPRINT')
            time.sleep(1.2)
            tampil.teks(text1='KEMUDIAN', text2='RESTART', text3='RASPBERRY')
            time.sleep(1.2)

    else:
        tampil.teks(text1='RASPBERRY MENGGUNAKAN', text2='%s BUAH FINGERPRINT' % len(useAlamat))
        while True:
            for alamat in useAlamat :
                Fingerprint.main_Program(alamat)
            

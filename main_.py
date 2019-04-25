from check_connection import connection_on
import lcd_
from rpidatabase import RpiDatabase
from rpidatabase import checking_table
def check_ip_config () :
    try :
        from instansi_id import ipaddress as ip
    except :
        from config import list_ip_fp as ip
    finally :
        return ip

ip_address = check_ip_config()
from config import list_used_ip_fp
def ping_ip (ip_address) :
    for i, alamat in enumerate(ip_address) :
        lcd_.progress_bar(i+1, len(ip_address), text='%s' % RpiDatabase().get_version())
        lcd_.disp.image(lcd_.image)
        lcd_.disp.display()
        if connection_on(alamat) :
            list_used_ip_fp.append(alamat)

if __name__ == '__main__' :
    from main_program import play
    from main_program import save_macaddress
    import time
    
    ping_ip(ip_address)
    save_macaddress()
    checking_table()
    if not list_used_ip_fp :
        lcd_.teks(text1='TIDAK ADA',text2='FINGERPRINT',text3='YANG TERHUBUNG')
        time.sleep(1.2)
        lcd_.teks(text1='HARAP HUBUNGKAN',text2='RASPBERRY',text3='KE FINGERPRINT')
        time.sleep(1.2)
        lcd_.teks(text1='KEMUDIAN', text2='RESTART', text3='RASPBERRY')
        time.sleep(1.2)
    else :
        lcd_.teks(text1='RASPBERRY MENGGUNAKAN', text2='%s BUAH FINGERPRINT' % len(list_used_ip_fp))
        while True :
            for ip_mesin in list_used_ip_fp :   
                print 'play'
                play(ip_mesin)

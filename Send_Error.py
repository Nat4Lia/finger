from Request_Retry_Session import requests_retry_session
import time

def send_error(data):
    t0 = time.time()
    try:
        response = requests_retry_session().post(   'http://eabsen.kalselprov.go.id/api/historycrash',
                                                    headers={'Content-Type':'applicetion/json','Accept':'application/json'}, 
                                                    json=data, 
                                                    timeout=5)
    except Exception as e:
        print 'Pengiriman Pesan Error Gagal :', e.__class__.__name__
    else:
        print 'Mengirimkan Pesan Error'
    finally:
        t1 = time.time()
        print 'Time', t1 - t0, 'seconds'
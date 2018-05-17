import time
import requests
from Send_Error import send_error
import json
import instansi_id
import logging
# import lcd_ as tampil

# logging.basicConfig(filename='APIERROR.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)
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

class METHOD:

    def __init__ (self):
        self.URL    =   'http://eabsen.kalselprov.go.id/api/'
        self.Header =   {
                            'Content-Type'  :   'application/json',
                            'Accept'        :   'application/json'
                        }

    def GET(self, URL, Timeout=5):
        try:
            r = requests.get(self.URL+URL, headers=self.Header, timeout=Timeout)
            if r.status_code == requests.codes.ok:
                Data = json.loads(r.content)
                return Data
            else :
                return None
        except (requests.exceptions.RequestException, ValueError, TypeError)  as err:
            # tampil.teks(text1="Server", text2=err.__class__.__name__)
            error = {'instansi_id' : instansi_id.ID_INSTANSI, 'keterangan' : err.__class__.__name__}
            send_error(error)
            logger.error(err)
            pass

    def POST(self, URL, Payload, Timeout=10):
        try:
            r = requests.post(self.URL+URL, headers=self.Header, json=Payload, timeout=Timeout)
            if r.status_code == requests.codes.ok and str(r.content) == str('Success') :
                return True
            else :
                return False
        except (requests.exceptions.RequestException, ValueError, TypeError)  as err:
            # tampil.teks( text1="Server", text2=err.__class__.__name__)
            error       = {'instansi_id' : instansi_id.ID_INSTANSI, 'keterangan' : err.__class__.__name__}
            send_error(error)
            logger.error(err)
            pass

class API(METHOD):
    def __init__ (self):
        METHOD.__init__(self)

    def PEGAWAI(self):
        return self.GET('cekpegawai/%s' % instansi_id.ID_INSTANSI)

    def TEMPLATE(self, pegawai_id):
        return self.GET('ambilfinger/%s' %pegawai_id)

    def TRIGGER(self):
        trigger = self.GET('triger')
        if trigger is not None:
            return trigger[0]['status']
        else:
            return trigger

    def ADMIN(self):
        return self.GET('admin/finger/')

    def VERSI(self):
        version = self.GET('version')
        if version is not None:
            return version['version']
        else:
            pass

    def MACADDRESS(self):
        return self.GET('macaddress')

    def HAPUS_PEGAWAI(self):
        return self.GET('hapusfingerpegawai')

    def LOG_RASPBERRY(self, payload):
        return self.POST('lograspberry', payload)

    def KEHADIRAN(self, payload):
        return self.POST('attendance', payload)

    def LOG_ERROR(self, payload):
        return self.POST('historycrash', payload)

    def GANTI_FINGER(self, IP):
        return self.GET('historyfinger/%s/%s' % (IP, instansi_id.ID_INSTANSI))

    def KONFIRM_GANTI_FINGER(self, payload):
        return self.POST('historyfinger', payload)

logger.error(API())
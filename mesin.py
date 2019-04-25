import requests
import json
import xml.etree.ElementTree as ET
from config import fp_payload

#logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# create a file handler
handler = logging.FileHandler('Error.log')
handler.setLevel(logging.ERROR)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
#

#Mesin
class Mesin:
    
#Inisialisasi
    def __init__ (self, ip_addr) :
        self.ip_addr        = ip_addr
        self.mac_address    = self.get_mac()#fungsi get_macaddress
        self.pegawai        = self.get_pegawai()#fungsi get_pegawai
        self.admin          = self.get_admin()#fungsi get_admin
        self.user           = self.get_user()#fungsi get_user
        self.attendance     = self.get_attendance()#fungsi get_att
# 

#Requests method (fp_payload['Command'] % (param 1,...,x)), return 'ConnectionError' or xml_data
    def method(self, payload) :
        #Mencoba untuk membuat request baru
        try :
            new_requests = requests.post(
                'http://%s:80/iWsService' % self.ip_addr,
                headers     = {'Content-Type'  :   'text/xml'},
                data        = payload,
                timeout     = 5
            )
            # print new_requests.content#debug
            return ET.fromstring(new_requests.content)
        except Exception as error :
            logger.error(error)
            return 'ConnectionError'
#

# get_mac, return None(fail) or macaddress_value 
    def get_mac(self) :
        try :
            _mac_address = self.method(fp_payload['GetOption'] % 'MAC')
            if _mac_address is 'ConnectionError' :
                raise Exception
            else :
                if _mac_address._children :
                    for row in _mac_address.findall('Row'):
                        return row.find('Value').text
                else :
                    raise Exception
        except Exception as error :
            logger.error(error)
            pass
#

# get_attendance, return None(fail) or [{}] json
    def get_attendance(self) :
        try :
            _attendance = self.method(fp_payload['GetAttLog'] % 'All')
            if _attendance is 'ConnectionError' :
                raise Exception
            else :
                PIN, TANGGAL, JAM, STATUS, ROW_ID = [], [], [], [], []
                for row_id, row in enumerate(_attendance.findall('Row')) :
                    PIN.append(row.find('PIN').text)
                    TANGGAL.append(row.find('DateTime').text.split()[0])
                    JAM.append(row.find('DateTime').text.split()[1])
                    STATUS.append(row.find('Status').text)
                    ROW_ID.append(row_id)

                absensi = [{'PIN'       : pin,
                            'Tanggal'   : tanggal,
                            'Jam'       : jam,
                            'Status'    : status,
                            'Row_ID'    : row_number
                            } for pin, tanggal, jam, status, row_number in zip (PIN, TANGGAL, JAM, STATUS, ROW_ID)]
                absen = json.loads(json.dumps(absensi))
                return absen
                #Jika Kosong akan return []
                #Jika Tidak Kosong akan return [{}]
                #Jika Koneksi Error akan return None
        except Exception as error :
            logger.error(error)
            pass
#   

# get_pegawai, return None(fail) or [{}] json
    def get_pegawai(self) :
        try:
            _pegawai = self.method(fp_payload['GetAllUserInfo'])
            if _pegawai is 'ConnectionError' :
                raise Exception
            else :
                PIN, NAMA, PASSWORD, PRIVILEGE = [], [], [], []
                for row in _pegawai.findall('Row') :
                    PIN.append(row.find('PIN2').text)
                    NAMA.append(row.find('Name').text)
                    PASSWORD.append(row.find('Password').text)
                    PRIVILEGE.append(row.find('Privilege').text)
                pegawai_dict = [{
                    'PIN'       : pin,
                    'Nama'      : nama,
                    'Password'  : password,
                    'Privilege' : privilege
                } for pin, nama, password, privilege in zip (PIN, NAMA, PASSWORD, PRIVILEGE)]    
                pegawai_json = json.loads(json.dumps(pegawai_dict))
                return pegawai_json
        except Exception as error :
            logger.error(error)
            pass
#

# get_user, return None(fail) or [{}] json
    def get_user(self) :
        _user = []
        if self.pegawai is None :
            pass
        else :
            for data in self.pegawai :
                if int (data['Privilege']) is 0 :
                    _user.append(data)
            return _user
#

# get_admin, return None(fail) or [{}] json
    def get_admin(self) :
        _admin = []
        if self.pegawai is None :
            pass
        else :
            for data in self.pegawai :
                if int (data['Privilege']) is 14 :
                    _admin.append(data)
            return _admin
#

# set_pegawai (pin, name, password), return True, False, None
    def set_user(self, pin, name, password = None) :
        try :
            if password : # Jika Menggunakan Password
                _registering = self.method(fp_payload['SetUserInfoPass'] % (name, password, pin))
            else : # Jika Menggunakan Sidik Jari
                _registering = self.method(fp_payload['SetUserInfoTem'] % (name, pin))
        
            if _registering is 'ConnectionError' :
                raise Exception
            else :
                for reply in _registering.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        return True 
                    else :
                        return False
        except Exception as error :
            logger.error(error)
            pass
#

# set_admin (pin, name, password), return boolean
    def set_admin(self, pin, name, password = None) :
        try :
            if password : # Jika Menggunakan Password
                _registering = self.method(fp_payload['SetAdminUserPass'] % (name, password, pin))
            else : # Jika Menggunakan Sidik Jari
                _registering = self.method(fp_payload['SetAdminUserTem'] % (name, pin))
        
            if _registering is 'ConnectionError' :
                raise Exception
            else :
                for reply in _registering.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        return True 
                    else :
                        raise Exception
        except Exception as error :
            logger.error(error)
            return False
#

# set_template (template->json type), return boolean
    def set_template(self, template) :
        _result = []
        try :
            for index, data in enumerate(template) :
                _registering_template = self.method(
                    fp_payload['SetUserTemplate'] % (
                        data['pegawai_id'],
                        index,
                        data['size'],
                        data['valid'],
                        data['templatefinger']
                    )
                )

                if _registering_template is 'ConnectionError' :
                    raise Exception
                else :
                    for reply in _registering_template.findall('Row') :
                        if reply.find('Information').text == 'Successfully!' :
                            _result.append(True)
                        else :
                            _result.append(False)
            return all(_result)
        except Exception as error :
            logger.error(error)
            pass            
#

# delete_user (pin), return boolean
    def delete_user(self, pin) :
        try :
            _delete_user = self.method(fp_payload['DeleteUser'] % pin)
            if _delete_user is 'ConnectionError' :
                raise Exception
            else :
                for reply in _delete_user.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        return True
                    else :
                        raise Exception
        except Exception as error :
            logger.error(error)
            return False
#

# delete_template (pin), return boolean
    def delete_template(self, pin) :
        try :
            _delete_template = self.method(fp_payload['DeleteTemplate'] % pin)
            if _delete_template is 'ConnectionError' :
                raise Exception
            else :
                for reply in _delete_template.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        return True
                    else :
                        raise Exception
        except Exception as error :
            logger.error(error)
            return False
#

# delete_password (pin), return boolean
    def delete_password(self, pin) :
        try :
            _delete_password = self.method(fp_payload['ClearUserPassword'] % pin)
            if _delete_password is 'ConnectionError' :
                raise Exception
            else :
                for reply in _delete_password.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        return True
                    else :
                        raise Exception
        except Exception as error :
            logger.error(error)
            return False
#

# clear_attendance, return boolean
    def clear_attendance(self) :
        try :
            _clear_attendance = self.method(fp_payload['ClearData'] % 3)
            if _clear_attendance is 'ConnectionError' :
                raise Exception
            else :
                for reply in _clear_attendance.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        _check_attendance = self.get_attendance()
                        if _check_attendance is 'ConnectionError' or _check_attendance:
                            raise Exception
                        else :
                            return True
                    else :
                        raise Exception
        except Exception as error:
            logger.error(error)
            return False
#

# clear_all, return boolean
    def clear_all(self) :
        import time
        try :
            _clear_all = self.method(fp_payload['ClearData'] % 1)
            if _clear_all is 'ConnectionError' :
                raise Exception
            else :
                for reply in _clear_all.findall('Row') :
                    if reply.find('Information').text == 'Successfully!' :
                        print 'ok'
                        time.sleep(10)
                        _check_attendance = self.get_attendance()
                        _check_pegawai = self.get_pegawai()
                        print _check_pegawai, _check_attendance
                        if _check_attendance is None or _check_pegawai is None or _check_attendance or _check_pegawai:
                            raise Exception
                        else :
                            return True
                    else :
                        raise Exception
        except Exception as error :
            logger.error(error)
            return False
#

# check_fingerprint
    def check_fingerprint(self, pin) :
        try :
            fingerprint = []
            for fingerid in range (0,2) :
                data = self.method(fp_payload['GetUserTemplate'] % (pin, fingerid))
                if data is not 'ConnectionError' :
                    if data._children :
                        fingerprint.append(True)
                    else :
                        fingerprint.append(False)
            if all(fingerprint) :
                return True
            else :
                return False
        except Exception as error :
            logger.error(error)
            pass
#

# check_user
    def check_user(self, who_check) :
        import time
        try :
            if self.pegawai :
                for data in self.pegawai :
                    if   (str(who_check) == str(data['PIN']) and str(data['Password']) != 'None') :
                        return True
                    elif (str(who_check) == str(data['PIN']) and str(data['Password']) == 'None') :
                        _check_fingerprint = self.check_fingerprint(who_check)
                        if _check_fingerprint is True :
                            return True
                        elif _check_fingerprint is False:
                            hapus = self.delete_user(who_check)
                            if hapus :
                                return False
                            else :
                                raise Exception
                        elif _check_fingerprint is None :
                            raise Exception
                    else :
                        continue
                return False
            elif not self.pegawai :
                return False
            elif self.pegawai is None :
                raise Exception
                
        except Exception as error :
            logger.error(error)
            # print error
            pass
#

# + get_attendance : return json
# + get_pegawai : return json
# + get_template : return json
# + get_admin : return json
# + get_user : return json
# + set_admin : return json
# + set_user : return True
# + set_template : return True
# + delete_template : return True
# + delete_user : return True
# + clear_attendance : return True
# + clear_all : return True
# + check_user


#

# template = [{"id":1116,"pegawai_id":7239,"size":"968","valid":"1","templatefinger":"SotTUzIxAAADyM0ECAUHCc7QAAAbyWkBAAAAg3UcXcgZABEPTADcAIrHoAAmAJIPuwAkyJUP4wBMAFAPrMhWAJAP9wCdAJ3HpQBzABMPVAB5yIwPxACCAFYPiMiYAI8PWwBsAIDHPQCqAAIPeQCsyBgPNQDDAL0PjsjCABQPwQAUAJrHhwDSAIkPUQARyZIPvwATAecPV8gZAXcP7ADZAaLHxAA6ASoPQgBCyZMP+wBHAeoPvMhPAaYPQQCTAVrHdQBcAYoPKImBtXqD9XkH9Tr7bckmBXuD7gVHhXjFAPpnBUMHh3xMzB78eQpHD6IT4kE\/hIKB5X37ANA0g4E3fJ8EfwQxt8t\/foBnDDb1ykd\/gHd3ooH2iNjN1Hvz9BPzeIwtT179ooFzhq4Tyry+\/vvz7nP+AAijm\/rik2uAwudU6ybnE3RrgIJ4ok0TCj+ISgh+APgmBpDfBs+LYH1k3p6HL9H359rL0TB+MacX0lZ7CCPxAAJWIfkMxYAC2ELBQ\/\/A+84AacoOQlBKDwD3BQU2wcIxwlfCjwYDlAQQSsAEAOcMBYkCAKgME8HGACTeCMAQAFAayf2EN0T\/wkTBFcUTIshFwf3\/XEC+VsPFAQ8t\/ThXlGcWyA45+kBPwKH\/wTdFWxYAB0gxMMP2WcD\/wv3BkMH9xQEIUf1ewTo\/RN8BCFkDbS+SOMCEWlsLAAxkOFT8CP5TAwCoccrAFMgFcvD9S1SY\/0CeRMAWAAx6Pz3DjlVFwcA+b8IAy00WZEsLAAFC+lQ3RkYLAAeTMsH+n\/5GDQCPm9JXwwhcwGQZAANk8DuIVUf\/RsPAOMHDmw4ACqnwNjr+\/QjARkoEADhvenDbAUCtBsE+pf5hN0doCQC\/stLAw5xWBAAxv3qyFQPMwPTBKVTAOkBVnP8GADnCAAVADciQxBNEwEqGYAbIMMZ0wMHDzgCBHIJRwcNpwM8AiRwS\/8D+wWAFGQPK8uT\/Mz3ABf42CMHBN\/\/AWdUAAjXm\/8D+\/\/4F\/0IINxcQAwri8P\/+Cf7+QEP\/\/zvD\/p4MEJINnIlFwvwKfwgQwxMekUsP2JEUkGLCiQTAwcERmBQawP46NsDPEVAVfYfEBQgTdxYkWMBMDNVYG85BTP7\/YQfVUBi\/w\/\/DhgQQKh8nnxAQBS\/X\/PP+MAg\/OwoQhj1fkMaxwQQQyD0roAoTS0KTwv7EoE0FE0NFHFgREBKJ1v4I\/P\/\/\/\/vBOMD8CP9VBhBxWFbDx2QFEHBej6vJEJmon3fAwsSgBQoTRmKawMLAwwHEj8sRTmbw+wA=","created_at":"2017-11-25 00:23:39","updated_at":"2017-11-25 00:23:39"},{"id":1117,"pegawai_id":7239,"size":"1494","valid":"1","templatefinger":"TJVTUzIxAAAF1tcECAUHCc7QAAAd12kBAAAAhXs3hdYdAIQPagDmAADZNgA4AHIPQQA61oUP2QBYAF4PHdZbAGQPSgCYAHfYaABhAHwOSwBn1ocPVABjAD4OsdZpAJQPNgC2AGXZ2gB2AKIPIgBz1igPdwCDALEPq9aHAJIPxwBDACzZgQCRAG4PgQCW1loO\/gCXAG4PFtabAE4PWwBfAFHZNQCjAN4OvgCt1h0OzwCqAPsPmNaqAJQP\/ABqADLZiACwACMOtQCw1jMPzAC6AHkPNtbJAD0PrAAMAKLZvQDWAJYPAwDd1mcO4wDZAI8PR9beADMPqAAaAJvYAgHhAL0PUwDj1hEPuQDtADcPwdbwAIQPiwA2AB3ZMAAAAS8PtgAC1xwOggAHAd8OhdYTAaAO8gDQAWPZ9AAcAdkPYQAu1wIP1gA3ASkPYtY\/AZ4PHACXASfYvABTAYIPFQBQ1\/gPbgBdAVQPdFQ7ATcDcYJbgupAPwNvEDd5fwE315+CJvgWdJMKP9D+9CP1JHurFBMugIGKDDYJdwV72wP2HIuBgTedM9IXbXYSAvDLZVfT4XtFe54IHYsDRscBNQhyIXv59Ly7AEIC2Zr4iwdDvPxdVkpMQH403Nf9GXZ+hrIIO6cu9BPxufqXJTvvhIYukeahvPjEOiyyiYT6FY8LYKcb7XJ5DY4L+6Y69AhVkdXy6BhMxPfhjYAOWN8oaNkHYRPm9RHkCveW9TOF8Vn6YdN0oFzmuedCjBuS8C2jBQdXVZEUCgR4T3R\/iRNaCPhko3shnHMtVpBeiUHAIrHzRQh8AssqJ\/0X9lcXoASEqksErH\/p\/PwGrV18hK6ISI6\/f+58WXYK7nMf02euViLp3vTybr8WH9q6Aa+CV4eiky4hBInemquAyHlX2ir7qvTTk37z82kGPSCeZSCPAQbLKwwQAHEA1V04nP\/C\/YAFAHYBFegGAK4GE\/8FRRHWWwkAQP9HOsDF6MHA\/sP7A8VDDqzACgCtDhaRwPsXVREAeBQPklTF6FU8BAA\/E7JcA9ZOGHdiwArFbiTW\/v4+\/0sIxWYnVmjAeAoAbuIDNZz\/wQQAMzaygw7WYTMGPT3BOcEB1jI7cGkKALs+hhZ5wsBtBgDCP+iXwA0AWCsAhf9BKVYmABtY64P9xZH\/QMD\/S8E4\/\/oWPS79NP\/+7woF7lj0\/0E4wMIAQ411wMOABQCLW\/L9CADdXCJUOlAG1hZeYMAIAIJhdVDBixAAsmJWZ8QXwMF5wHcFxZJh2cEsFgC4a9tUMOj+\/v0uIyrDADekZcF4GAA1smCDvHXDYsGEg0QDBT12J8AFAN+\/K8TuCADneivBh\/49ywFzgneSwgeW+lXAhZDDYosFHgV6g5rDwIPDB8DGFsLBwcDBwQTC+hTAwMLBdcLbAM5QJf48T8AhO\/z45f7+Pf78\/T8bG9ariJfCdZYHwcYXwMHAwcLBBcDHF8PAw\/\/DYMAAt1wl\/v\/ADwACiiyd\/8D8\/8D8Pvz6Kw0AfI56xADBxlrDcRUASI8h\/vsr\/0D+\/Tv9PPf+KEMGAISSD+bAJta7wrSIwsMFxZMVmsHD\/sLAvcLGKY10lwsAfFFxwRXCw8LBdQnFQ5KB\/pmABQASWFDFFf4bAFedVlfDcRbAwcLAxG4Hw8UVf4kkAM2laHzHFcGDwv+iwQfBxBZ\/wsDBwW8HwIbGAdOtNzPAPvv5K\/z\/\/sA2BcWNqvb+ggcAcLES+f0oLgQBALI0hAQFLLI6ZAUAbnw6jNMBzr49\/cA8CgXlykDC\/8LCOogN1sTbXPkgOcAAh2IsgAoA49yD\/\/kr\/\/z8wP0TxUPm4sB4wYbCZwR4xtIAD\/dMKQrEA+Cf\/8D8OCcExZrsxZoMAAP0OgWAbBR1BxA1AjAEwMRCERAwAzTBRcLEFsP\/i4cFELYLIRX+xAURBxeb\/j3REfAYZDsxwhBulxLC\/4sDEDJIdSgEEBdIGsBDAxUkU3fABxDqmXr6jcEA","created_at":"2017-11-25 00:24:53","updated_at":"2017-11-25 00:24:53"}]
# new_mesin = Mesin('10.10.10.40')
# print new_mesin.check_fingerprint(5977)
# print new_mesin.delete_password(1)
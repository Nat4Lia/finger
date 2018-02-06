import requests
import time
import lcd_ as cetak


get = {
        'GetAttLog'         : '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></GetAttLog>',
        'GetUserTemplate'   : '<GetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID></Arg></GetUserTemplate>',
        'GetUserInfo'       : '<GetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></GetUserInfo>',
        'SetUserInfo'       : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group></Group><Privilege></Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
        'DeleteUser'        : '<DeleteUser><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteUser>',
        'GetAllUserInfo'    : '<GetAllUserInfo><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey></GetAllUserInfo>',
        'SetUserTemplate'   : '<SetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID><Size>%s</Size><Valid>%s</Valid><Template>%s</Template></Arg></SetUserTemplate>',
        'ClearData'         : '<ClearData><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><Value xsi:type=\"xsd:integer\">%s</Value></Arg></ClearData>',
        'GetOption'         : '<GetOption><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><Name xsi:type=\"xsd:string\">%s</Name></Arg></GetOption>',
        'DeleteTemplate'    : '<DeleteTemplate><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteTemplate>',
        'SetAdminUser'      : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group></Group><Privilege>14</Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>'
      }


# URL = 'http://10.10.10.10/iWsService'

def POST (URL, header, payload) :
    while True:
        try:
            time.sleep(2)
            r = requests.post(URL, headers=header, data=payload)
            if str(r.headers['Content-Type']) == 'text/xml':
                return r
            else:
                cetak.printLCD('Gagal Terhubung','Dengan Fingerprint').lcd_status()
                cetak.printLCD('Mencoba','Menghubungkan...').lcd_status()
        except requests.exceptions.RequestException as err:
            cetak.printLCD('Gagal Terhubung','Dengan Fingerprint').lcd_status()
            cetak.printLCD('Mencoba','Menghubungkan...').lcd_status()
            pass
        except requests.exceptions.Timeout as err:
            cetak.printLCD('Gagal Terhubung','Dengan Fingerprint').lcd_status()
            cetak.printLCD('Mencoba','Menghubungkan...').lcd_status()
            pass
        except requests.exceptions.ConnectionError as err:
            cetak.printLCD('Gagal Terhubung','Dengan Fingerprint').lcd_status()
            cetak.printLCD('Mencoba','Menghubungkan...').lcd_status()
            pass
        except requests.exceptions.HTTPError as err:
            cetak.printLCD('Gagal Terhubung','Dengan Fingerprint').lcd_status()
            cetak.printLCD('Mencoba','Menghubungkan...').lcd_status()
            pass
        except requests.exceptions.ConnectTimeout as err:
            cetak.printLCD('Gagal Terhubung','Dengan Fingerprint').lcd_status()
            cetak.printLCD('Mencoba','Menghubungkan...').lcd_status()
            pass

class inisialisasi_alamat:
    def __init__(self, tujuan, alamat):
        self.tujuan = tujuan
        self.url = 'http://%s/iWsService' % alamat
        self.header = {'Content-Type' : 'text/xml'}
        self.comKey = 0

class fingerprint(inisialisasi_alamat):
    def __init__(self, tujuan, alamat):
        inisialisasi_alamat.__init__(self, tujuan, alamat)

    def Option(self,option):
        payload = get['GetOption'] % (self.comKey, option)
        return POST (self.url, self.header, payload).content
    
    def GetAttLog(self,pin):
        payload = get['GetAttLog'] % (self.comKey, pin)
        return POST (self.url, self.header, payload).content
    
    def GetUserTemplate(self, pin, templateid):
        payload = get['GetUserTemplate'] % (self.comKey, pin, templateid)
        return POST (self.url, self.header, payload).content

    def GetUserInfo(self, pin):
        payload = get['GetUserInfo'] % (self.comKey, pin)
        return POST (self.url, self.header, payload).content

    def SetUserInfo(self, nama, pin):
        payload = get['SetUserInfo'] % (self.comKey, nama, pin)
        return POST (self.url, self.header, payload).content

    def DeleteUser(self, pin):
        payload = get['DeleteUser'] % (self.comKey, pin)
        return POST (self.url, self.header, payload).content

    def GetAllUserInfo(self):
        payload = get['GetAllUserInfo'] % (self.comKey)
        return POST (self.url, self.header, payload).content

    def SetUserTemplate(self, pin, fingerid, size, valid, template):
        payload = get['SetUserTemplate'] % (self.comKey, pin, fingerid, size, valid, template)
        return POST (self.url, self.header, payload).content

    def DeleteTemplate(self, pin):
        payload = get['DeleteTemplate'] % (self.comKey, pin)
        return POST (self.url, self.header, payload).content

    def SetAdminUser(self, nama, pin):
        payload = get['SetAdminUser'] % (self.comKey, nama, pin)
        return POST (self.url, self.header, payload).content

    def ClearData(self, clearcode):
        payload = get['ClearData'] % (self.comKey, clearcode) #$ClearCode (1=SEMUA, 2=TEMPLATE?, 3=RECORD)
        try:
            requests.post(self.url, headers=self.header, data=payload)
        except requests.exceptions.RequestException as err:
            pass
        except requests.exceptions.Timeout as err:
            pass
        except requests.exceptions.ConnectionError as err:
            pass
        except requests.exceptions.HTTPError as err:
            pass
        except requests.exceptions.ConnectTimeout as err:
            pass
    
# print fingerprint('Finger A', '10.10.10.10').GetAllUserInfo()
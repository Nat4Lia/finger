import httplib, urllib, urllib2
import re
import xml.etree.ElementTree as ET
import mysql.connector
import time
import requests
import json
import string
import subprocess
import socket
import check_connection

#GETATTLOG = $comKey, $PIN
#GETUSERTEMPLATE = $comKey, $PIN, $FingerID
#GETUSERINFO = $comKey, $PIN
#SETUSERINFO = $comKey, $NAMA, $PIN2
#DELETEUSER = $comKey, $PIN
#SETUSERTEMPLATE = $comKey, $PIN, $FingerID, $SIZE, $VALID, $TEMPLATE
#CLEARDATA = $comKey, $ClearCode (1=RECORD, 2=TEMPLATE?, 3=ALL)

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

class getDataFinger:

    def __init__(self, teks, alamat, comKey):
        self.conn = httplib.HTTPConnection(alamat)
        self.comKey = comKey
        self.teks = teks
        self.alamat = alamat
        self.tryAlamat = 'http://%s' % alamat

class deleteTemplate(getDataFinger):
    def __init__(self, teks, alamat, comKey, pin):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.pin = pin

    def delete(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['DeleteTemplate'] % (self.comKey, self.pin)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            return responRead
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class getOption(getDataFinger):
    def __init__(self, teks, alamat, comKey, option):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.option = option

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['GetOption'] % (self.comKey, self.option)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            userData = ET.fromstring(responRead)
            return userData[0][0].text
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class getAttLog(getDataFinger):
    def __init__(self, teks, alamat, comKey, userID):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.userID = userID

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['GetAttLog'] % (self.comKey, self.userID)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            return response.read()
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class getUserTemplate(getDataFinger):
    def __init__(self, teks, alamat, comKey, userID, fingerID):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.userID = userID
        self.fingerID = fingerID

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['GetUserTemplate'] % (self.comKey, self.userID, self.fingerID)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            userData = ET.fromstring(responRead)
            return responRead
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class getUserInfo(getDataFinger):
    def __init__(self, teks, alamat, comKey, userID):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.userID = userID

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['GetUserInfo'] % (self.comKey, self.userID)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            userData = ET.fromstring(responRead)
            return responRead
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class setUserInfo(getDataFinger):
    def __init__(self, teks, alamat, comKey, nama, pin2):
        getDataFinger.__init__(self, teks, alamat, comKey)
        # self.pin1 = pin1
        self.nama = nama
        self.pin2 = pin2

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['SetUserInfo'] % (self.comKey, self.nama, self.pin2)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}

            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            return responRead
            # status = ET.fromstring(responRead)
            # return status[0][1].text
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class setAdminUser(getDataFinger):
    def __init__(self, teks, alamat, comKey, nama, pin2):
        getDataFinger.__init__(self, teks, alamat, comKey)
        # self.pin1 = pin1
        self.nama = nama
        self.pin2 = pin2

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['SetAdminUser'] % (self.comKey, self.nama, self.pin2)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}

            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            return responRead
            # status = ET.fromstring(responRead)
            # return status[0][1].text
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class delUser(getDataFinger):
    def __init__(self, teks, alamat, comKey, userID):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.userID = userID

    def delete(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['DeleteUser'] % (self.comKey, self.userID)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            return responRead
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class getAllUserInfo(getDataFinger):
    def __init__(self, teks, alamat, comKey):
        getDataFinger.__init__(self, teks, alamat, comKey)

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['GetAllUserInfo'] % (self.comKey)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            return responRead
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class setUserTemplate(getDataFinger):
    def __init__(self, teks, alamat, comKey, userID, fingerID, size, valid, template):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.userID = userID
        self.fingerID = fingerID
        self.size = size
        self.valid = valid
        self.template = template

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['SetUserTemplate'] % (self.comKey, self.userID, self.fingerID, self.size, self.valid, self.template)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
            response = self.conn.getresponse()
            responRead = response.read()
            return responRead
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

class clearData(getDataFinger):
    def __init__(self, teks, alamat, comKey, command):
        getDataFinger.__init__(self, teks, alamat, comKey)
        self.command = command

    def get(self):
        global get
        try :
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            cookies = response.getheader("set-cookie")
            XML = get['ClearData'] % (self.comKey, self.command)
            headers = { "Content-type": "text/xml",
                        "Content-Length": "%d" % len(XML)}
            self.conn.request("POST", "/iWsService HTTP1.0", "", headers)
            self.conn.send(XML)
        except httplib.HTTPException as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.error as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
        except socket.timeout as err:
            check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

        # response = self.conn.getresponse()
        # responRead = response.read()
        # status = ET.fromstring(responRead)
        # return

class getMAC (getDataFinger):
    def __init__(self, teks, alamat, comKey):
        getDataFinger.__init__(self, teks, alamat, comKey)

    def get(self):
        MAC = None
        while MAC is None:
            try:
                response = getOption(self.teks, self.alamat, self.comKey,'MAC').get()
                MAC = ET.fromstring(response)
                return MAC[0][0].text
            except httplib.HTTPException as err:
                check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
            except socket.error as err:
                check_connection.onCheck(self.teks, self.tryAlamat, 5).check()
            except socket.timeout as err:
                check_connection.onCheck(self.teks, self.tryAlamat, 5).check()

# comKey = 0
# userID = 'All'
# XML = (('<GetAttLog>'
#         '<ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey>'
#             '<Arg>'
#                 '<PIN xsi:type=\"xsd:integer\">%s</PIN>'
#             '</Arg>'
#         '</GetAttLog>'))
#
# _XML = XML % (comKey, userID)
#
# print _XML

# print get['GetAttLog']

# response = getAttLog(0,'All').get()
# print response

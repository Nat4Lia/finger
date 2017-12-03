import httplib, urllib, urllib2
import socket
import re
import lcd_

class check_Connection:
    alamaturl = 'alamaturl'

    def __init__ (self, tujuan, waktuhabis):
        self.tujuan = tujuan
        self.waktuhabis = waktuhabis

class onCheck (check_Connection) :

    def __init__ (self, teks, tujuan, timeout):
        check_Connection.__init__ (self, tujuan, timeout)
        self.teks = teks

    def check(self):
        while True:
            try:
                urllib2.urlopen(self.tujuan, timeout=self.waktuhabis)
                print 'PING   : OK !'
                return True
            except urllib2.URLError as err:
                lcd_.printLCD('URL','Error').lcd_status()
                lcd_.printLCD('Try to connect',self.teks).lcd_status()
                print 'Try to connect %s' % self.teks
            except socket.timeout as err:
                lcd_.printLCD('Socket','Timeout').lcd_status()
                lcd_.printLCD('Try to connect',self.teks).lcd_status()
                print 'Try to connect %s' % self.teks
            except socket.error as err:
                lcd_.printLCD('Socket','Error').lcd_status()
                lcd_.printLCD('Try to connect',self.teks).lcd_status()
                print 'Try to connect %s' % self.teks

    def checkAlamat(self):
        try:
            print self.tujuan
            urllib2.urlopen(self.tujuan, timeout=self.waktuhabis)
            print 'PING   : OK !'
            return True
        except urllib2.URLError as err:
            return False
        except socket.timeout as err:
            return False
        except socket.timeout as err:
            return False

internet = onCheck('Server Eabsen','http://eabsen.kalselprov.go.id',5)

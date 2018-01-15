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
                return True
            except urllib2.URLError as err:
                lcd_.printLCD('Gagal Terhubung','Ke %s' % self.teks).lcd_status()
                lcd_.printLCD('Mencoba Terhubung','Ke %s' % self.teks).lcd_status()
            except socket.timeout as err:
                lcd_.printLCD('Gagal Terhubung','Ke %s' % self.teks).lcd_status()
                lcd_.printLCD('Mencoba Terhubung','Ke %s' % self.teks).lcd_status()
            except socket.error as err:
                lcd_.printLCD('Gagal Terhubung','Ke %s' % self.teks).lcd_status()
                lcd_.printLCD('Mencoba Terhubung','Ke %s' % self.teks).lcd_status()

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

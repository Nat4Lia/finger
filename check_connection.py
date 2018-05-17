import urllib2

def connection_on(address):
    try:
        urllib2.urlopen('http://%s' % address, timeout=1)
        return True
    except urllib2.HTTPError:
        return False
    except Exception:
        return False

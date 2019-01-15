import os

def connection_on(address) :
    response = os.system("ping -c 3 " + address)
    if response == 0:
        return True
    else:
        return False

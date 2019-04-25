from config import server_url
from config import skpd
import requests
import logging
import json

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

class API :

    def __init__ (self) :
        self.json_header    =   {   'Content-Type'  :   'application/json',
                                    'Accept'        :   'application/json'  } 

    def get_server (self, api_param, time_out = 5) :
        try :
            receive = requests.get(
                server_url+'/api/'+api_param, 
                headers = self.json_header, 
                timeout = time_out
            )
            
            if receive.status_code is requests.codes.ok :
                receive_json = json.loads(receive.content)
                return receive_json
            else :
                return None
            
        except (requests.exceptions.RequestException, ValueError, TypeError) as error:
            if error.__class__.__name__ == 'ReadTimeOut' :
                print 'Server Sibuk'
            elif error.__class__.__name__ == "ConnectionError" :
                print 'Tidak Bisa Mengakses Server'
            logger.error(error)
            return 'ServerConnectionError'

    def post_server (self, api_param, payload, time_out = 10) :
        try :
            receive = requests.post(
                server_url+'/api/'+api_param, 
                headers = self.json_header, 
                json=payload,
                timeout = time_out
            )
            #ganti == dengan is
            if receive.status_code == requests.codes.ok and str(receive.content) == str('Success') :
                return 'Success'
            elif receive.status_code == requests.codes.ok and str(receive.content) == str('Failed') :
                return 'Failed'
            else :
                raise requests.exceptions.RequestException
        except (requests.exceptions.RequestException, ValueError, TypeError) as error:
            if error.__class__.__name__ == 'ReadTimeOut' :
                print 'Server Sibuk'
            elif error.__class__.__name__ == "ConnectionError" :
                print 'Tidak Bisa Mengakses Server'
            
            logger.error(error)
            return 'ServerConnectionError'

    def post_return_data (self, api_param, payload, time_out = 10) :
        try :
            receive = requests.post(
                server_url+'/api/'+api_param, 
                headers = self.json_header, 
                json=payload,
                timeout = time_out
            )
            #ganti == dengan is
            if receive.status_code == requests.codes.ok :
                receive_json = json.loads(receive.content)
                return receive_json
            else :
                raise requests.exceptions.RequestException
        except (requests.exceptions.RequestException, ValueError, TypeError) as error:
            print error.__class__.__name__
            if error.__class__.__name__ == 'ReadTimeOut' :
                print 'Server Sibuk'
            elif error.__class__.__name__ == "ConnectionError" :
                print 'Tidak Bisa Mengakses Server'

            logger.error(error)
            return 'ServerConnectionError'



# print API().post_fp('10.10.10.10', fp_payload['GetUserInfo'] % ('All'))
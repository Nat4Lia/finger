import requests
import json
from collections import namedtuple

from .const import *
from .exception import APIErrorConnection, APIErrorResponse, APINetworkError


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class API(object) :

    def __init__ (self) : 
        self.header = REQUEST_HEADER
        self.eabsen = EABSEN_URL
        self.request_post = REQUEST_POST
        self.request_get = REQUEST_GET
        self.full_url = None

    def send(self, request_type, api_url, params='', data=None) :
        try :
            if request_type == self.request_get :
                r = requests.get('{}{}{}'.format(self.eabsen, api_url, params), timeout=5, headers=self.header, stream=True)
            elif request_type == self.request_post :
                r = requests.post(self.eabsen+api_url, timeout=5, headers=self.header, json=data)
            if r.status_code != 200 : 
                raise APIErrorResponse('Server Status Code : {}'.format(r.status_code))
            if r.headers['Content-Type'] == 'text/html; charset=UTF-8' : return str(r.content)
            elif r.headers['Content-Type'] == 'application/json' : return json2obj(r.content)
        except Exception as e:
            raise APIErrorConnection(str(e))

    def post_rpi_status(self, data) :
        return self.send('POST',POST_RASPBERRY_STATUS,data=data)

    def post_att(self, data) :
        return self.send('POST',POST_ATTENDANCE,data=data)

    def post_user_queue(self, data) :
        return self.send('POST',POST_QUEUE,data=data)

    def get_user_queue(self, data) :
        return self.send('POST',GET_QUEUE,data=data)

    def get_user(self, param) :
        return self.send('GET', GET_USER, params=param)

    def get_auth(self, param) :
        return self.send('GET', GET_AUTHENTICATION, params=param)

    def get_admin(self) :
        return self.send('GET', GET_ADMIN)

    def get_trigger(self) :
        return self.send('GET', GET_TRIGGER)
    
    def get_version(self) :
        return self.send('GET', GET_VERSION)

    def get_reg_mac(self) :
        return self.send('GET', GET_REGISTERED_MACADDRESS)

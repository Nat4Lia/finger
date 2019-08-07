
import requests
import json
import xml.etree.ElementTree as ET
from collections import namedtuple

from .const import *
from .exception import SOAPErrorConnection, SOAPErrorResponse, SOAPNetworkError
from .attendance import Attendance
from .user import User
from .template import Template

class SOAP(object) :

    def __init__ (self, ip) :
        self.ip = ip

    def send(self, data) :
        try :
            r = requests.post(URL % self.ip, headers=HEADER, data=data, timeout=5)
            # print r.content
            # return ET.fromstring(r.content)
            if r.status_code == 200 : 
                return {'status' : True,
                        'response' : ET.fromstring(r.content)}
            else :
                return {'status' : False,
                        'response' : ET.fromstring(r.content)}
        except Exception as e:
            raise SOAPErrorConnection(str(e))

    def get_att(self) :
        """
        :return: the machine's Attendance
        """
        attendances = []
        response = self.send(GET_ATT_LOG.format('All'))
        if response["status"] :
            for row_id, row in enumerate(response["response"].findall('Row')) :
                attendance = Attendance(row.find('PIN').text, row.find('DateTime').text.split()[0], row.find('DateTime').text.split()[1], row.find('Status').text, row_id)
                attendances.append(attendance)
            return attendances
        else :
            raise SOAPErrorResponse("Can't read response")
        
    def get_users(self) :
        """
        :return: the machine's Users
        """
        users = []
        response = self.send(GET_ALL_USER_INFO)
        if response["status"] :
            for row in response["response"].findall('Row') :
                if int(row.find('Privilege').text) == USER :
                    user = User(row.find('PIN2').text, row.find('Name').text, row.find('Password').text, row.find('Privilege').text, row.find('PIN').text)
                    users.append(user)
            return users
        else :
            raise SOAPErrorResponse("Can't read response")

    def get_admins(self) :
        """
        :return: the machine's Admins
        """
        users = []
        response = self.send(GET_ALL_USER_INFO)
        if response["status"] :
            for row in response["response"].findall('Row') :
                if int(row.find('Privilege').text) == ADMIN :
                    user = User(row.find('PIN2').text, row.find('Name').text, row.find('Password').text, row.find('Privilege').text, row.find('PIN').text)
                    users.append(user)
            return users
        else :
            raise SOAPErrorResponse("Can't read response")

    def get_user(self, user_id) :
        """
        :return: the machine's User
        """
        users = []
        response = self.send(GET_USER_INFO.format(user_id))
        if response["status"] :
            for row in response["response"].findall('Row') :
                if int(row.find('Privilege').text) == USER :
                    user = User(row.find('PIN2').text, row.find('Name').text, row.find('Password').text, row.find('Privilege').text, row.find('PIN').text)
                    users.append(user)
            return users
        else :
            raise SOAPErrorResponse("Can't read response")

    def get_user_templates(self, user_id, total_template) :
        """
        :return: the machine's User Templates
        """
        templates = []
        for template_id in range (0, total_template) :
            response = self.send(GET_USER_TEMPLATE.format(user_id, template_id))
            if response["status"] :
                for row in response["response"].findall('Row') :
                    template = Template(row.find('PIN').text, row.find('Size').text, row.find('Valid').text, row.find('Template').text, row.find('FingerID').text)
                    templates.append(template)
            else :
                raise SOAPErrorResponse("Can't read response")
        if all(templates) :
            return templates
        else :
            raise SOAPErrorResponse("Can't read template")

    def set_user_template(self, user_id, template_id, size, valid, template) :
        """
        :return bool: True if response Successfully!
        """
        set_user_template = self.send(SET_USER_TEMPLATE.format (user_id, template_id, size, valid, template))
        if set_user_template["status"] :
            for row in set_user_template["response"].findall('Row') :
                if (row.find('Information').text) == 'Successfully!' : return True
        else :
                raise SOAPErrorResponse("Can't read response")

    def set_user(self, user_id, nama, privilege, password='') :
        """
        :return bool: True if response Successfully!
        """
        set_user = self.send(SET_USER_INFO_PASSWORD.format (nama, password, privilege, user_id))
        if set_user["status"] :
            for row in set_user["response"].findall('Row') :
                if (row.find('Information').text) == 'Successfully!' : return True
        else :
                raise SOAPErrorResponse("Can't read response")

    def delete_user(self, user_id) :
        """
        :return bool: True if response Successfully!
        """
        del_user = self.send(DELETE_USER.format (user_id))
        if del_user["status"] :
            for row in del_user["response"].findall('Row') :
                if (row.find('Information').text) == 'Successfully!' : return True
        else :
                raise SOAPErrorResponse("Can't read response")
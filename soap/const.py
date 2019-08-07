"""
URL AND HEADER
"""
URL                     = 'http://%s:80/iWsService'
HEADER                  = {'Content-Type'  :   'text/xml'}
"""
MACHINE SOAP COMMAND
"""

GET_OPTION              = '<GetOption><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Name xsi:type=\"xsd:string\">{}</Name></Arg></GetOption>'
GET_ATT_LOG             = '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN></Arg></GetAttLog>'
GET_USER_TEMPLATE       = '<GetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN><FingerID xsi:type=\"xsd:integer\">{}</FingerID></Arg></GetUserTemplate>'    
GET_USER_INFO           = '<GetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">{}</PIN></Arg></GetUserInfo>'
GET_ALL_USER_INFO       = '<GetAllUserInfo><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey></GetAllUserInfo>'
SET_USER_INFO_PASSWORD  = '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>{}</Name><Password>{}</Password><Group></Group><Privilege>{}</Privilege><Card></Card><PIN2>{}</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>'
SET_USER_INFO_TEMPLATE  = '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>{}</Name><Password></Password><Group></Group><Privilege>{}</Privilege><Card></Card><PIN2>{}</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>'
SET_USER_TEMPLATE       = '<SetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN><FingerID xsi:type=\"xsd:integer\">{}</FingerID><Size>{}</Size><Valid>{}</Valid><Template>{}</Template></Arg></SetUserTemplate>'
DELETE_USER             = '<DeleteUser><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">{}</PIN></Arg></DeleteUser>'
DELETE_TEMPLATE         = '<DeleteTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN></Arg></DeleteTemplate>'
CLEAR_DATA              = '<ClearData><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Value xsi:type=\"xsd:integer\">{}</Value></Arg></ClearData>'
CLEAR_USER_PASSWORD     = '<ClearUserPassword><ArgComKey xsi:type="xsd:integer">0</ArgComKey><Arg><PIN xsi:type="xsd:integer">{}</PIN></Arg></ClearUserPassword>'

"""
USER PRIVILEGE
"""
ADMIN                   = 14
USER                    = 0

"""
CLEAR DATA CODE
"""
CLEAR_ALL               = 1
CLEAR_TEMPLATE          = 2
CLEAR_ATT               = 3

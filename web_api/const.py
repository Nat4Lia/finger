"""
EABSEN URL
"""
EABSEN_URL                          ='http://eabsen.test'#'http://eabsen.kalselprov.go.id'
EABSEN_DOMAIN                       ='eabsen.test'

"""
API URL
"""
GET_USER                            = '/api/cekpegawai/'
GET_AUTHENTICATION                  = '/api/ambilfinger/'
GET_ADMIN                           = '/api/admin/finger'
GET_TRIGGER                         = '/api/triger'
GET_VERSION                         = '/api/version'
GET_REGISTERED_MACADDRESS           = '/api/macaddress'
GET_QUEUE                           = '/api/queuepegawai/get'

POST_ATTENDANCE                     = '/api/attendance'
POST_RASPBERRY_STATUS               = '/api/lograspberry'
POST_QUEUE                          = '/api/queuepegawai/post'

"""
TRIGGER COMMAND
"""
NORMAL                              = 1
VALIDATION_EMPLOYEE                 = 2
UPDATE_PROGRAM                      = 3
CLEAR_ATTENDANCE_TABLE_BY_INSTANSI  = 4
CUSTOM_DISTRIBUTION_BY_INSTANSI     = 5

"""
DISTRIBUTION COMMAND
"""
NEW_REGISTRATION                    = 'daftar'
CHANGE_AUTHENTICATION               = 'ganti'
REMOVE_USER                         = 'hapus'

"""
REQUEST
"""
REQUEST_HEADER                      = {'Content-Type':'application/json','Accept':'application/json'}
REQUEST_POST                        = 'POST'
REQUEST_GET                         = 'GET'
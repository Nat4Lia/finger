from instansi_id import ID_INSTANSI
versi_software      =   '3.0'
server_url          =   'http://eabsen.kalselprov.go.id'
skpd                =    ID_INSTANSI
mysql_config        = {
                        'user': 'root',
                        'password': 'eabsen.kalselprov.go.id',
                        'host': 'localhost',
                        'database': 'data_finger',
                        'raise_on_warnings': True,
}

attendance_table    =   {
                            'table' : {
                                'name'  : 'attendance',
                                'column' : [
                                    {
                                        'name'      : 'id',
                                        'structure' : 'bigint(20) not null auto_increment primary key',
                                        'index'     : []
                                    },
                                    {
                                        'name'      : 'mac_',
                                        'structure' : 'varchar(20) null',
                                        'index'     : [
                                            'pencarian'
                                        ]

                                    },
                                    {
                                        'name'      : 'row_id',
                                        'structure' : 'int(11) null',
                                        'index'     : [
                                            'pencarian'
                                        ]
                                    },
                                    {
                                        'name'      : 'user_pin',
                                        'structure' : 'int(50) not null',
                                        'index'     : []
                                    },
                                    {
                                        'name'      : 'tanggal',
                                        'structure' : 'date null',
                                        'index'     : []
                                    },
                                    {
                                        'name'      : 'jam',
                                        'structure' : 'time null',
                                        'index'     : []
                                    },
                                    {
                                        'name'      : 'status',
                                        'structure' : 'int(11) null',
                                        'index'     : []
                                    },
                                    {
                                        'name'      : 'flag',
                                        'structure' : 'varchar(15) null',
                                        'index'     : [
                                            'pencarian'
                                        ]
                                    }
                                ],
                                'index' : [
                                    {
                                        'name'  : 'pencarian',
                                    }
                                ]
                            }
}

maccaddress_table   =   {
                            'table' : {
                                'name' : 'macaddress',
                                'column' : [
                                    {
                                        'name' : 'id',
                                        'structure' : 'int(11) not null auto_increment primary key',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'mac_',
                                        'structure' : 'varchar(20) not null',
                                        'index'     : []
                                    }
                                    
                                ],
                                'index' : []
                            }
}

version_table       =   {
                            'table' : {
                                'name' : 'version',
                                'column' : [
                                    {
                                        'name' : 'version',
                                        'structure' : 'varchar(20) not null',
                                        'index'     : []
                                    }  
                                ],
                                'index' : []
                        }
}

server_api_param    =   {
                            'Pegawai'       :   'cekpegawai/%s' % skpd,
                            'Autentikasi'   :   'ambilfinger/%s',
                            'Admin'         :   'admin/finger',
                            'Trigger'       :   'triger',
                            'Versi'         :   'version',
                            'Macaddress'    :   'macaddress',
                            'Absensi'       :   'attendance',
                            'Status'        :   'lograspberry',
                            'GetQueue'      :   'queuepegawai/get',
                            'PostQueue'     :   'queuepegawai/post'
}
 
fp_payload          =   {  
                            'GetAttLog'         : '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></GetAttLog>',
                            'GetUserTemplate'   : '<GetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID></Arg></GetUserTemplate>',
                            'GetUserInfo'       : '<GetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></GetUserInfo>',
                            'SetUserInfoPass'   : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password>%s</Password><Group>1</Group><Privilege></Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
                            'SetUserInfoTem'    : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group>1</Group><Privilege></Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
                            'DeleteUser'        : '<DeleteUser><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteUser>',
                            'GetAllUserInfo'    : '<GetAllUserInfo><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey></GetAllUserInfo>',
                            'SetUserTemplate'   : '<SetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID><Size>%s</Size><Valid>%s</Valid><Template>%s</Template></Arg></SetUserTemplate>',
                            'ClearData'         : '<ClearData><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Value xsi:type=\"xsd:integer\">%s</Value></Arg></ClearData>',
                            'GetOption'         : '<GetOption><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Name xsi:type=\"xsd:string\">%s</Name></Arg></GetOption>',
                            'DeleteTemplate'    : '<DeleteTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteTemplate>',
                            'SetAdminUserTem'   : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group></Group><Privilege>14</Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
                            'SetAdminUserPass'  : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password>%s</Password><Group></Group><Privilege>14</Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
                            'ClearUserPassword' : '<ClearUserPassword><ArgComKey xsi:type="xsd:integer">0</ArgComKey><Arg><PIN xsi:type="xsd:integer">%s</PIN></Arg></ClearUserPassword>'
}

list_ip_fp          =   [
                            '10.10.10.10',
                            # '10.10.10.20',
                            # '10.10.10.30',
                            # '10.10.10.40',
                            # '10.10.10.50',
                            # '10.10.10.11',
                            # '10.10.10.12',
                            # '10.10.10.13',
                            # '10.10.10.14',
                            # '10.10.10.15',
]

list_used_ip_fp     =   [

]

SQL_SYNTAX = {
                'ADDPEGAWAI' 	      : 'INSERT INTO pegawai (user_pin2, user_name, mac_) VALUES (%s, %s, %s)',
                'ADDADMIN' 		      : 'INSERT INTO pegawaiAdmin (user_pin2, user_name, mac_) VALUES (%s, %s, %s)',
                'ADDMAC'		      : 'INSERT INTO macaddress (mac_) VALUES (%s)',
                'ADDATTENDANCE'	      : 'INSERT INTO attendance (user_pin, mac_) VALUES (%s, %s)',
                'ADDVERSION'          : 'INSERT INTO version (version) VALUES (%s)',
                'CHECKATTENDANCE'     : 'SELECT COUNT(*) FROM attendance WHERE mac_ = (%s)',
                'CHECKPEGAWAI'	      : 'SELECT COUNT(*) FROM pegawai WHERE mac_ = (%s)',
                'CHECKADMIN'	      : 'SELECT COUNT(*) FROM pegawaiAdmin WHERE mac_ = (%s)',
                'CHECKMAC'		      : 'SELECT COUNT(*) FROM macaddress',
                'CHECKALLATTENDANCE'  : 'SELECT COUNT(*) FROM attendance',
                'CHECKALLADMIN'       : 'SELECT COUNT(*) FROM pegawaiAdmin',
                'CHECKALLPEGAWAI'     : 'SELECT COUNT(*) FROM pegawai',
                'CHECKVERSION'        : 'SELECT version FROM version',
                'DELETEMAC'	      	  : 'DELETE FROM macaddress WHERE mac_ = (%s)',
                'DELETEPEGAWAI'	      : 'DELETE FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'DELETEPEGAWAIID'	  : 'DELETE FROM pegawai WHERE id = (%s) AND mac_ = (%s)',
                'DELETEADMIN'	      : 'DELETE FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'DELETEADMINID'	      : 'DELETE FROM pegawaiAdmin WHERE id = (%s) AND mac_ = (%s)',
                'DELETEATTENDANCE'    : 'DELETE FROM attendance WHERE mac_ = (%s)',
                'FINDMAC'		      : 'SELECT mac_ FROM macaddress WHERE mac_ = (%s)',
                'FINDALLMAC'          : 'SELECT mac_ FROM macaddress',
                'FINDALLADMIN'	      : 'SELECT user_pin2 FROM pegawaiAdmin WHERE mac_ = (%s)',
                'FINDADMIN'		      : 'SELECT user_pin2 FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDPEGAWAI'	      : 'SELECT user_pin2 FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDPEGAWAIALL'      : 'SELECT * FROM pegawai WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDADMINALL'        : 'SELECT * FROM pegawaiAdmin WHERE user_pin2 = (%s) AND mac_ = (%s)',
                'FINDALLPEGAWAI'      : 'SELECT user_pin2 FROM pegawai WHERE mac_ = (%s)',
                'UPDATEVERSION'       : 'UPDATE version SET version = %s',
                'TRUNCATE'		      : 'TRUNCATE TABLE attendance'
}
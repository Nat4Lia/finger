"""
TABLE
"""
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

device_info_table         =   {
                            'table' : {
                                'name' : 'device_info',
                                'column' : [
                                    {
                                        'name' : 'id',
                                        'structure' : 'int(11) not null auto_increment primary key',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'ip',
                                        'structure' : 'varchar(20)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'mac',
                                        'structure' : 'varchar(20)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'sn',
                                        'structure' : 'varchar(20)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'firmware',
                                        'structure' : 'varchar(50)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'finger_version',
                                        'structure' : 'varchar(10)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'users',
                                        'structure' : 'int(20)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'fingers',
                                        'structure' : 'int(20)',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'passwords',
                                        'structure' : 'int(20) null',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'records',
                                        'structure' : 'int(20) null',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'created_at',
                                        'structure' : 'timestamp not null default now()',
                                        'index'     : []
                                    },
                                    {
                                        'name' : 'updated_at',
                                        'structure' : 'timestamp not null default now() on update now()',
                                        'index'     : []
                                    }
                                ],
                                'index' : []
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

"""
CONFIG
"""
config              = {
                        'user': 'root',
                        'password': 'root',
                        'host': 'localhost',
                        'database':'data_finger',
                        'raise_on_warnings': True,
}
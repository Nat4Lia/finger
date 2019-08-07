import mysql.connector
from collections import namedtuple

from .const import *
from .exception import DBErrorConnection, DBErrorResponse

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

#Class RpiDatabase
class RpiDatabase(object):

    def __init__ (self, config = config) :
        try:
            self.cnx        = mysql.connector.connect(**config)
            self.cursor     = self.cnx.cursor(buffered = True)
            self.cnx.commit()
        except (Exception, mysql.connector.errors.DatabaseError) as e:
            if e.errno == 1049 :
                x = self.is_db_exists('root', 'root', 'localhost')
                if x :
                    self.cnx        = mysql.connector.connect(**config)
                    self.cursor     = self.cnx.cursor(buffered = True)
                    self.cnx.commit()
            else :
                raise DBErrorConnection(str(e))
        finally :
            self.checking_table()

    def is_db_exists(self, uname, password, db_host, dbname=config['database']) :
        cnx        = mysql.connector.connect(user = uname, password = password, host = db_host)
        cursor     = cnx.cursor(buffered = True)
        this = cursor
        this.execute(
            """CREATE DATABASE IF NOT EXISTS {0}
            """
            .format(dbname)
        )
        cnx.close()
        return True

    def is_table_exists(self, tablename, dbname = config['database']) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}' AND
                  table_schema = '{1}'
            """.format(
                    tablename.replace('\'', '\'\''), 
                    dbname.replace('\'', '\'\'')
                )
        )
        if this.fetchone()[0] == 1:
            return True
        return False

    def is_column_exists(self, tablename, columnname) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_name = '{0}' AND
                  column_name = '{1}'
            """.format(
                    tablename.replace('\'', '\'\''), 
                    columnname.replace('\'', '\'\'')
                )
        )
        if this.fetchone()[0] == 1:
            return True
        return False

    def is_index_exists(self, tablename, indexname, dbname = config['database']) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(1) indexExists 
            FROM INFORMATION_SCHEMA.STATISTICS 
            WHERE 
                table_schema='{0}' AND 
                table_name='{1}' AND 
                index_name='{2}' 
            """.format(
                    dbname.replace('\'', '\'\''), 
                    tablename.replace('\'', '\'\''),
                    indexname.replace('\'', '\'\'')
                )
        )
        if this.fetchone()[0] > 0 :
            return True
        return False

    def create_table(self, table) :
        try:
            this = self.cursor
            column_string = ""
            index_string = ""
            column_index = ""
            for column in table['table']['column'] :
                column_string += column['name']+" "+column['structure']+", "
            this.execute(
                """
                CREATE TABLE IF NOT EXISTS {0} (
                    {1}
                )
                """.format(
                        table['table']['name'],
                        column_string[:-2]
                    )
            )
            for index in table['table']['index'] :
                index_string += index['name']
                for column in table['table']['column'] :
                    for indexing_column in column['index'] :
                        if indexing_column is index['name'] :
                            column_index += column['name']+", "                    
                this.execute(
                    """
                    CREATE INDEX {0}
                    ON {1} ({2})
                    """.format(index_string, table['table']['name'], column_index[:-2])
                )
            return True
        except Exception as error :
            if str(error).find('1050') is 0:
                return False

    def create_column(self, table, column, structure) :
        this = self.cursor
        this.execute(
            """
            ALTER TABLE {0}
                ADD {1} {2}
            """.format (
                table, column, structure
            )
        )

    def create_index(self, index, table, columnlist) :
        this = self.cursor
        this.execute(
            """
            CREATE INDEX {0}
            ON {1} ({2})
            """.format( index, table, columnlist)
        )

    def is_table_zero (self, table) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(id) FROM {0}
            """.format(table)
        )
        count = this.fetchone()[0]
        if count is None :
            pass
        elif count > 0:
            return True
        else:
            return False

    def truncate(self, table) :
        this = self.cursor
        this.execute(
            """
            TRUNCATE TABLE {0}
            """.format(table)
        )
        self.cnx.commit()
        return

    def insert (self, table, column, value) :
        this = self.cursor
        this.execute(
            """
            INSERT INTO {0} ({1})
            VALUES ('{2}')
            """.format(table, column, value)
        )
        self.cnx.commit()

    def is_version_same (self, version) :
        this = self.cursor
        this.execute(
            """
            SELECT version
            FROM version
            """
        )
        _get_version = this.fetchone()[0]
        if _get_version is None :
            return False
        else :
            if _get_version == version :
                return True
            else :
                return False

    def update_version(self, version_value) :
        this = self.cursor
        this.execute(
            """
            UPDATE version
            SET version = '{0}'
            """.format(version_value)
        )
        self.cnx.commit()

    def get_version(self) :
        this = self.cursor
        this.execute(
            """
            SELECT version FROM version
            """
        )
        value = this.fetchone()[0]
        if value is None :
            pass
        else :
            return value

    def is_macaddress_registered (self, macaddress_value) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(*)
            FROM macaddress
            WHERE mac_ = '{0}'
            """.format(macaddress_value)
        )
        if this.fetchone()[0] is 1 :
            return True
        else :
            return False

    def delete_macaddress(self, mac) :
        this = self.cursor
        this.execute(
            """
            DELETE FROM macaddress
            WHERE mac_ = '{0}'
            """.format(mac)
        )
        self.cnx.commit()

    def count_macaddress(self) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(*)
            FROM macaddress
            """
        )
        count = this.fetchone()[0]
        if count is None :
            pass
        else :
            return count

    def get_all_mac(self) :
        this = self.cursor
        this.execute(
            """
            SELECT mac_ FROM macaddress
            """
        )
        macaddress = this.fetchall()
        _macaddress = []
        for data in macaddress :
            _macaddress.append(data[0])

        return _macaddress

    def insert_absensi(self, mac, row_id, user_pin, tanggal, jam, status, flag) :
        this = self.cursor
        this.execute(
            """
            SELECT COUNT(*)
            FROM attendance 
            WHERE   mac_    = '{0}' AND
                    row_id  = '{1}'
            """.format(mac, row_id)
        ) #is_row_exists?

        if this.fetchone()[0] == 1 :#if exists, update
            this.execute(
                """
                UPDATE attendance
                SET flag = '{0}'
                WHERE row_id = '{1}'
                """.format(flag, row_id)
            )
            self.cnx.commit()
        else :#if new
            this.execute(
                """
                INSERT INTO attendance(
                    mac_, row_id, user_pin, tanggal, jam, status, flag
                ) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                """.format(mac, row_id, user_pin, tanggal, jam, status, flag)
            )
            self.cnx.commit()

    def get_failed_flag(self, mac, flag='Failed') :
        if mac is not None :
            this = self.cursor
            this.execute(
                """
                SELECT row_id
                FROM attendance
                WHERE mac_ = '{0}' AND flag = '{1}'
                """.format(mac, flag)
            )
            return this.fetchall()
        else :
            pass

    def get_success_flag(self, mac, flag='Success') :
        if mac is not None :
            this = self.cursor
            this.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                WHERE mac_ = '{0}' AND flag = '{1}'
                """.format(mac, flag)
            )
            return this.fetchone()[0]
        else :
            pass

    def get_all_attendace_sent(self, mac) :
        this = self.cursor
        if mac is not None :
            this.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                WHERE mac_ = '{0}'
                """.format(mac)
            )
            count = this.fetchone()[0]
            return count
        else :
            pass

    def delete_by_mac(self, macaddress) :
        this = self.cursor
        this.execute(
            """
            DELETE FROM attendance
            WHERE mac_ = '{}'
            """.format(macaddress)
        )
        self.cnx.commit()

    def i_device_info(self, device) :
        d = namedtuple("device", device.keys())(*device.values())
        this = self.cursor
        try :
            this.execute(
                "SELECT COUNT(*) FROM device_info WHERE mac = '{}'".format(d.mac)
            ) #is_row_exists?

            if this.fetchone()[0] == 1 :#if exists, update
                this.execute(
                    """
                    UPDATE device_info
                    SET ip = '{}',firmware = '{}', finger_version = '{}',users = '{}',
                        fingers = '{}',passwords = '{}',records = '{}'
                    WHERE mac = '{}'
                    """.format(
                        d.ip, d.firmware, d.finger_version, d.users,
                        d.fingers, d.passwords, d.records, d.mac
                    )
                )
                self.cnx.commit()
            else :#if new
                this.execute(
                    """
                    INSERT INTO device_info(
                        ip, mac, sn, firmware, finger_version, users, fingers, passwords,records
                    ) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')
                    """.format(
                        d.ip, d.mac, d.sn, d.firmware, d.finger_version,
                        d.users, d.fingers, d.passwords, d.records
                    )
                )
        except Exception as e :
            raise DBErrorResponse(str(e))
        finally :
            self.cnx.commit()

    def checking_table(self, table_check = [attendance_table, device_info_table, maccaddress_table, version_table]) :
        # check table
        try :
            import time
            # lcd_.teks(text1='CHECKING',text2='DATABASE')
            print 'cek database'
            for index, structure in enumerate(table_check) :
                if self.is_table_exists(structure['table']['name']) :
                    for column in structure['table']['column'] :
                        if self.is_column_exists(
                                structure['table']['name'], 
                                column['name']
                        ) : 
                            continue
                        else: 
                            self.create_column(
                                structure['table']['name'],
                                column['name'],
                                column['structure']
                            )   
                    for index in structure['table']['index'] :
                        if self.is_index_exists(
                            structure['table']['name'], 
                            index['name']
                        ) :
                            continue
                        else :
                            column_index = ""
                            for column in structure['table']['column'] :
                                for indexing_column in column['index'] :
                                    if indexing_column is index['name'] :
                                        column_index += column['name']+", " 
                            self.create_index(
                                index['name'],
                                structure['table']['name'],
                                column_index[:-2]
                            )
                else :
                    self.create_table(structure)
            # lcd_.teks(text1='DATABASE',text2='READY')
            print 'database_ready'
            time.sleep(1.2)
        except Exception as error:
            print error
            # logger.error(error)
            # lcd_.teks(text1='DATABASE',text2='NOT READY')
            # time.sleep(1.2)
            print 'database not ready'

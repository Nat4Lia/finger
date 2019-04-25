from config import mysql_config
from config import attendance_table
from config import maccaddress_table
from config import version_table
import mysql.connector
import lcd_

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

#Class RpiDatabase
class RpiDatabase :

#Insisalisasi
    def __init__ (self, config = mysql_config) :
        self.cnx        = mysql.connector.connect(**config)
        self.cursor     = self.cnx.cursor(buffered = True)
        self.cnx.commit()
        self.version_now= self.get_version()
        self.count_mac  = self.count_macaddress()
#

# is_table_exists(tablename, dbname=database config), return True or False
    def is_table_exists(self, tablename, dbname = mysql_config['database']) :
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
#

# is_column_exists (tablename, columnname), return True or False
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
#

# is_index_exists() : return True
    def is_index_exists(self, tablename, indexname, dbname = mysql_config['database']) :
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
#

# create_table() : return True
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
            logger.error(error)
            if str(error).find('1050') is 0:
                return False
#

# create column
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
#

# create index
    def create_index(self, index, table, columnlist) :
        this = self.cursor
        this.execute(
            """
            CREATE INDEX {0}
            ON {1} ({2})
            """.format( index, table, columnlist)
        )
#

# truncate
    def truncate(self, table) :
        this = self.cursor
        this.execute(
            """
            TRUNCATE TABLE {0}
            """.format(table)
        )
        self.cnx.commit()
#

# insert
    def insert (self, table, column, value) :
        this = self.cursor
        this.execute(
            """
            INSERT INTO {0} ({1})
            VALUES ('{2}')
            """.format(table, column, value)
        )
        self.cnx.commit()
#

# is_version_same
    def is_version_same (self, version) :
        this = self.cursor
        this.execute(
            """
            SELECT version
            FROM version
            """
        )
        _get_version = this.fetchone()[0]
        if this.fetchone() is None :
            return False
        else :
            if _get_version is version :
                return True
            else :
                return False
#

# update_version
    def update_version(self, version_value) :
        this = self.cursor
        this.execute(
            """
            UPDATE version
            SET version = '{0}'
            """.format(version_value)
        )
        self.cnx.commit()
#

# get_version
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
#

# is_macaddress_registered
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
        
#

# delete_mac
    def delete_macaddress(self, mac) :
        this = self.cursor
        this.execute(
            """
            DELETE FROM macaddress
            WHERE mac_ = '{0}'
            """.format(mac)
        )
        self.cnx.commit()
#

# count_macaddress
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
#

# get_all_mac
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
            _macaddress.append(macaddress[0][0])

        return _macaddress
#

# insert_absensi
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
#

# get_failed_flag
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
#

# get_all
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
#

# delete_by_mac
    def delete_by_mac(self, macaddress) :
        this = self.cursor
        this.execute(
            """
            DELETE FROM attendance
            WHERE mac_ = '{0}'
            """.format(macaddress)
        )
        self.cnx.commit()
#


# RpiDatabase = RpiDatabase()
# print RpiDatabase.get_failed_flag('AA')

def checking_table(table_check = [attendance_table, maccaddress_table, version_table]) :
    # check table
    try :
        import time
        lcd_.teks(text1='CHECKING',text2='DATABASE')
        time.sleep(1.2)
        for index, structure in enumerate(table_check) :
            if RpiDatabase().is_table_exists(structure['table']['name']) :
                for column in structure['table']['column'] :
                    if RpiDatabase().is_column_exists(
                            structure['table']['name'], 
                            column['name']
                    ) : 
                        continue
                    else: 
                        RpiDatabase().create_column(
                            structure['table']['name'],
                            column['name'],
                            column['structure']
                        )   
                for index in structure['table']['index'] :
                    if RpiDatabase().is_index_exists(
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
                        RpiDatabase().create_index(
                            index['name'],
                            structure['table']['name'],
                            column_index[:-2]
                        )
            else :
                RpiDatabase().create_table(structure)
        lcd_.teks(text1='DATABASE',text2='READY')
        time.sleep(1.2)
    except Exception :
        logger.error(error)
        lcd_.teks(text1='DATABASE',text2='NOT READY')
        time.sleep(1.2)


#
# + is_table_exists (tablename): return True
# + is_column_exists (columnname): return True
# + is_index_exists : return True
# + is_table_ready (table : json) : return True
# + change_column (table : json) : return True
# + create_table (table : json) : return True
# + create_column (table : json) : return True
# + create_index (table : json) : return True
# + truncate (table) : return True
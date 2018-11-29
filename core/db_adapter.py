from helpers.singleton import *
from settings import settings
from peewee import MySQLDatabase


db_schema = settings.SETTINGS['DATABASE']['SCHEMA']
INFO_SCHEMA_COLUMN_LIST = [
    "table_catalog",
    "table_schema",
    "table_name",
    "column_name",
    "ordinal_position",
    "column_default",
    "is_nullable",
    "data_type",
    "character_maximum_length",
    "character_octet_length",
    "numeric_precision",
    "numeric_scale",
    "character_set_name",
    "collation_name",
    "column_type",
    "column_key",
    "extra",
    "privileges",
    "column_comment"
]


@Singleton
class MySQLDbAdapter(object):
    """
    Database adapter for peewee ORM
    """

    isConnected = False
    db_instance = None
    statements = {
        'list_tables': 'SELECT table_name FROM information_schema.tables WHERE table_schema = "' +
                       db_schema + '"',
        'list_table_properties': 'SELECT ' + ','.join(INFO_SCHEMA_COLUMN_LIST) +
                                 ' FROM information_schema.columns WHERE table_schema = "' +
                                 db_schema + '" AND TABLE_NAME = "{}";'
    }

    __settings__ = settings.SETTINGS['DATABASE']

    def connect(self):
        """
        Connects to the specified DB
        Returns:
        """
        db_settings = self.__settings__

        self.db_instance = MySQLDatabase(db_settings['SCHEMA'],
                                         host=db_settings['HOST'],
                                         port=int(db_settings['PORT']),
                                         user=db_settings['USER'],
                                         passwd=db_settings['PASSWORD'])
        self.db_instance.connect()
        
        if self.db_instance is not None:
            self.isConnected = True

    def close(self, req=None, resp=None):
        """
        Close the db connection
        Args:
            req:
            resp:
        Returns:
        """
        if self.db_instance is not None and self.isConnected:
            try:
                self.db_instance.close()
                self.isConnected = False
            except AttributeError:
                print(req, resp)
                pass

    def create_tables(self, tables):
        """
        Args:
            tables: list
        Returns:
        """
        if self.isConnected:
            table_list = []
            for table in tables:
                if not table.table_exists():
                    table_list.append(table)
            self.db_instance.create_tables(table_list)

            for cr_table in table_list:
                if len(cr_table.initial_data) != 0:
                    for in_data in cr_table.initial_data:
                        cr_table().add(in_data)


mysql_adapter = MySQLDbAdapter.Instance()

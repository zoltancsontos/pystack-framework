from helpers.singleton import *
from settings import settings
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase
from core.orm.db_type import DbType
import operator


@Singleton
class DbAdapter(object):
    """
    Database adapter for peewee ORM
    """

    isConnected = False
    db_instance = None

    __settings__ = settings.SETTINGS['DATABASE']

    def connect(self):
        """
        Connects to the specified DB
        Returns:
        """
        self.__set_db_instance__()
        self.db_instance.connect()
        if self.db_instance is not None:
            self.isConnected = True

    def __set_db_instance__(self):
        """
        Sets the database instance based on config
        :return:
        """
        db_settings = self.__settings__
        db_type = db_settings['ADAPTER_TYPE']
        if db_type == DbType.MYSQL:
            self.db_instance = MySQLDatabase(db_settings['SCHEMA'],
                                             host=db_settings['HOST'],
                                             port=int(db_settings['PORT']),
                                             user=db_settings['USER'],
                                             passwd=db_settings['PASSWORD'])
        elif db_type == DbType.POSTGRES:
            self.db_instance = PostgresqlDatabase(db_settings['SCHEMA'],
                                                  host=db_settings['HOST'],
                                                  port=int(db_settings['PORT']),
                                                  user=db_settings['USER'],
                                                  password=db_settings['PASSWORD'])
        elif db_type == DbType.SQLLITE:
            self.db_instance = SqliteDatabase('app.db')

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
                pass

    def create_tables(self, tables):
        """
        Args:
            tables: list
        Returns:
        """
        sorted_tables = sorted(tables, key=operator.attrgetter('__name__'))
        if self.isConnected:
            table_list = []
            for table in sorted_tables:
                if not table.table_exists():
                    table_list.append(table)
            self.db_instance.create_tables(table_list)

            for cr_table in table_list:
                if len(cr_table.initial_data) != 0:
                    for in_data in cr_table.initial_data:
                        cr_table().add(in_data)


db_adapter = DbAdapter.Instance()

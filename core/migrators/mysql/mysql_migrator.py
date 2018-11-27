from helpers.general_helpers import GeneralHelpers
from core.db_adapter import mysql_adapter
from core.migrators.sql_statements import SqlStatements
from core.migrators.mysql.information_schema import InformationSchema
from core.migrators.migrator_interface import MigratorInterface
from peewee import *


class MySqlMigrator(MigratorInterface):
    """
    Migrator class
    :author: Csontos_Zoltan@solarturbines.com
    :version: 1.0.0
    """
    db_proxy = Proxy()
    adapter = None
    db = None

    def set_connection(self):
        """
        Creates a db connection
        :return:
        """
        self.adapter = mysql_adapter
        self.adapter.connect()
        self.db_proxy.initialize(self.adapter.db_instance)
        self.db = self.db_proxy

    def close_connection(self):
        """
        Close the db connection
        :return:
        """
        self.db.close()

    def get_current_table_list(self):
        """
        Returns the list of current tables
        :return: list<dict>
        """
        db_tables = []
        sql = self.adapter.statements['list_tables']
        cursor = self.db.execute_sql(sql)
        for item in cursor.fetchall():

            column_name = item[0]

            table_prop_sql = self.adapter.statements['list_table_properties'].format(column_name)
            table_prop_cursor = self.db.execute_sql(table_prop_sql)
            prop_list = []

            for prop in table_prop_cursor.fetchall():
                info_schema = InformationSchema(prop)
                prop_list.append({
                    'column_name': info_schema.column_name,
                    'type': info_schema.column_type,
                    'default': info_schema.column_default,
                    'null': info_schema.is_nullable,
                    'extra': info_schema.extra
                })

            db_tables.append({
                'table_name': column_name,
                'columns': prop_list
            })

        return db_tables

    def get_current_models_data_dump(self):
        """
        Returns the current db dump
        :return:
        """
        tables = self.get_current_table_list()
        table_map = []

        for table in tables:

            statement = 'SELECT * FROM ' + table['table_name'] + ';'
            cursor = self.db.execute_sql(statement)
            single_table_data = []

            for item in cursor.fetchall():
                single_table_data.append(item)

            table_map.append({
                'table_name': table['table_name'],
                'columns': table['columns'],
                'data': single_table_data
            })

        return table_map

    @staticmethod
    def __process_single_statement__(table_name, cols, data):
        """
        Generates a single insert statement for a single row of data
        :param table_name:
        :param cols:
        :param data:
        :return:
        """
        col_list = []
        col_list_str = ', '

        for col in cols:
            col_list.append(col['column_name'])

        col_list_str = col_list_str.join(col_list)
        safe_data = str(data).replace('None', '"None"')

        statement = 'INSERT INTO ' + table_name + ' (' + col_list_str + ') VALUES ' + safe_data + ';'
        return statement

    def get_data_backup_statements(self):
        """
        Get the list of insert statements to be able to restore the db
        :return: str
        """
        statements = [
            'SET FOREIGN_KEY_CHECKS=0;'
        ]
        table_map_data = self.get_current_models_data_dump()

        for single_data in table_map_data:

            statements.append('TRUNCATE TABLE ' + single_data['table_name'] + ';')
            statements.append('ALTER TABLE ' + single_data['table_name'] + ' AUTO_INCREMENT = 1;')

            for data in single_data['data']:
                statement = MySqlMigrator.__process_single_statement__(
                    single_data['table_name'],
                    single_data['columns'],
                    data
                )
                statements.append(statement)

        statements.append('SET FOREIGN_KEY_CHECKS=1;')
        sql_statements = SqlStatements(statements)
        return sql_statements

    def get_current_table_create_statements(self):
        """
        Returns the statement list of existing tables
        :return:
        """
        current_table_list = self.get_current_table_list()
        sql_statements = SqlStatements([])

        for table in current_table_list:
            cursor = self.db.execute_sql('SHOW CREATE TABLE ' + table['table_name'])
            data = cursor.fetchall()
            for item in data:
                column, statement = item
                sql_statements.push(statement)

        return sql_statements

    @staticmethod
    def process_all_models():
        """
        Process all models
        :return:
        """
        models = GeneralHelpers.get_models()
        for model in models:
            model_vars = vars(model)
            for item in model_vars:
                if '_' not in item:
                    print(item)

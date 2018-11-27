
class MigratorInterface(object):

    """
    Abstract interface for database migrators, all migrator classes should inherit this
    :@author: zoltan.csontos.dev@gmail.com
    :@version: 1.0.0
    """

    def set_connection(self):
        """
        Sets the connection to the selected database adapter
        :return:
        """
        raise NotImplementedError('set_connection() database connection method not implemented')

    def close_connection(self):
        """
        Closes connection to the selected database adapter
        :return:
        """
        raise NotImplementedError('close_connection() database close method not implemented')

    def get_current_table_list(self):
        """
        Returns the current table list
        :return:
        """
        raise NotImplementedError('get_current_table_list() method not implemented')

    def get_current_models_data_dump(self):
        """
        Returns the current models data dump
        :return:
        """
        raise NotImplementedError('get_current_models_data_dump() method not implemented')

    def get_data_backup_statements(self):
        """
        Returns the data backup statements
        :return:
        """
        raise NotImplementedError('get_data_backup_statements() method not implemented')

    def get_current_table_create_statements(self):
        """
        Returns the list of create table statements
        :return:
        """
        raise NotImplementedError('get_current_table_create_statements() method not implemented')

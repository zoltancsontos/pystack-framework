import os
import re
env = os.environ


class DbHelpers(object):
    """
    Database helpers
    :author: zoltan.csontos.dev@gmail.com
    """

    @staticmethod
    def __get_connection_parts__(connection_string, ):
        conn_str = env['CLEARDB_DATABASE_URL']
        db_type, user, password, host, database = re.match('(.*?)://(.*?):(.*?)@(.*?)/(.*)', conn_str).groups()
        return db_type, user, password, host, database

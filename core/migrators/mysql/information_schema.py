class InformationSchema(object):

    """
    Object to hold the information schema data
    :author: zoltan.csontos.dev@gmail.com
    :version: 1.0.0
    """

    table_catalog = None
    table_schema = None
    table_name = None
    column_name = None
    ordinal_position = None
    column_default = None
    is_nullable = None
    data_type = None
    character_maximum_length = None
    character_octet_length = None
    numeric_precision = None
    numeric_scale = None
    character_set_name = None
    collation_name = None
    column_type = None
    column_key = None
    extra = None
    privileges = None
    column_comment = None

    def __init__(self, data):
        """
        Public constructor
        :param data: cursor dictionary
        :return:
        """
        self.table_catalog, \
            self.table_schema, \
            self.table_name, \
            self.column_name, \
            self.ordinal_position, \
            self.column_default, \
            self.is_nullable, \
            self.data_type, \
            self.character_maximum_length, \
            self.character_octet_length, \
            self.numeric_precision, \
            self.numeric_scale, \
            self.character_set_name, \
            self.collation_name, \
            self.column_type, \
            self.column_key, \
            self.extra, \
            self.privileges, \
            self.column_comment = data
class SqlStatements(object):
    """
    SQL Statements class
    :author: zoltan.csontos.dev@gmail.com
    :version: 1.0.0
    """
    statements = []

    def __init__(self, statements):
        """
        Public constructor
        :param statements:
        :return: void
        """
        self.statements = statements

    def to_string(self):
        """
        Returns the statements as string
        :return:
        """
        return "".join(self.statements)

    def get(self):
        """
        Returns the list of statements
        :return: list
        """
        return self.statements

    def set(self, statements):
        """
        Sets the list of statements
        :param statements:
        :return: void
        """
        self.statements = statements

    def push(self, item):
        """
        Adds a single item to statements list
        :param item: any
        :return: void
        """
        self.statements.append(item)
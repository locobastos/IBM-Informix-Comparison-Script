# coding=utf-8
from SharedFunctions import *
from Attribute import Attribute


class Table:
    """
    A table is described by :
        - The database on which it exists
        - Its name
        - Its owner
        - Its dictionnary of attributes
        - The chunk on which it is installed
        - Its extent rule
        - Its lock mode
    """

    def __init__(self, database, create_statement):
        """
        We create a new Table instance by giving it the database instance (usefull to get the
        database name from the table) and the create statement.
        :param database: The database instance
        :param create_statement: The create table statement
        """

        # Database instance
        self.database = database

        if "." in create_statement.split(' ', 3)[2]:
            # Table's name
            self.table_name = create_statement.split(' ', 3)[2].split('.')[1]

            # Table's owner
            self.table_owner = create_statement.split(' ', 2)[2].split('.')[0]
        else:
            # Table's name
            self.table_name = create_statement.split(' ', 3)[2]

            # Table's owner
            self.table_owner = create_statement.split(' ', 2)[2]

        # Dictionnary of attributes
        attributes_string = get_string_between_tags(create_statement, "(", ")")
        splitted_attributes = attributes_string.split(', ')
        self.attributes_dictionnary = {}
        for attribute in splitted_attributes:
            self.attributes_dictionnary[get_attribute_name(attribute)] = Attribute(self, attribute)

        # The chunk
        self.chunk = create_statement.split(' in ')[1].split(' ', 1)[0]

        # Extent rule
        post_chunk = create_statement.split(' in ')[1].split(' ')
        self.extent_rule = post_chunk[1] + " " + post_chunk[2] + " " + post_chunk[3] + " " + \
            post_chunk[4] + " " + post_chunk[5] + " " + post_chunk[6]

        # Lock mode rule
        self.lock_mode = post_chunk[7] + " " + post_chunk[8] + " " + post_chunk[9]

    def __eq__(self, other_table):
        """
        Two tables instances are equal only if all of their fields are equals.
        :param other_table: The other table instance to compare with
        :return: True if the two tables instances are equal
        """

        equal = self.table_name == other_table.table_name \
            and self.table_owner == other_table.table_owner \
            and self.chunk == other_table.chunk \
            and self.extent_rule == other_table.extent_rule \
            and self.lock_mode == other_table.lock_mode

        if equal:
            for attribute in list(self.attributes_dictionnary.keys()):
                attr_instance = self.attributes_dictionnary.get(attribute)
                if not attr_instance.__eq__(other_table.attributes_dictionnary.get(attribute)):
                    equal = False
                    break

        return equal


def get_attribute_name(attribute):
    """
    Return the attribute name from the attribute definition
    :param attribute: The attribute definition
    :return: The attribute's name
    """

    splitted_attribute = attribute.split(' ', 2)
    return splitted_attribute[0]

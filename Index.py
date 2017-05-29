# coding=utf-8
from SharedFunctions import *


class Index:
    """
    An index is described by :
        - The database on which it exists
        - Its name
        - Its unique constraint
        - Its owner
        - The list of the attributes
        - The table on which the index is created
        - The owner of the table on which the index is created
        - The chunk on which it is installed
    """

    def __init__(self, database, index_statement):
        """
        We create a new Index instance by giving it the database instance (usefull to get the
        database name from the index) and the create index statement.
        :param database: The database instance
        :param index_statement: The create index statement
        """

        splitted_statement = index_statement.split(' ', 6)

        # Database instance
        self.database = database

        # Its unique constraint
        if splitted_statement[1] == "unique":
            self.unique_constraint = "unique"
        else:
            self.unique_constraint = ""

        if self.unique_constraint:
            if "." in splitted_statement[3]:
                # Index's name
                self.index_name = splitted_statement[3].split('.')[1]

                # Index's owner
                self.index_owner = splitted_statement[3].split('.')[0]
            else:
                # Index's name
                self.index_name = splitted_statement[3]

                # Index's owner
                self.index_owner = splitted_statement[3]

            if "." in splitted_statement[5]:
                # The table on which the index is created
                self.on_table = splitted_statement[5].split('.')[1]

                # The owner of the table on which the index is created
                self.on_table_owner = splitted_statement[5].split('.')[0]
            else:
                # The table on which the index is created
                self.on_table = splitted_statement[5]

                # The owner of the table on which the index is created
                self.on_table_owner = splitted_statement[5]
        else:
            if "." in splitted_statement[2]:
                # Index's name
                self.index_name = splitted_statement[2].split('.')[1]

                # Index's owner
                self.index_owner = splitted_statement[2].split('.')[0]
            else:
                # Index's name
                self.index_name = splitted_statement[2]

                # Index's owner
                self.index_owner = splitted_statement[2]

            if "." in splitted_statement[4]:
                # The table on which the index is created
                self.on_table = splitted_statement[4].split('.')[1]

                # The owner of the table on which the index is created
                self.on_table_owner = splitted_statement[4].split('.')[0]
            else:
                # The table on which the index is created
                self.on_table = splitted_statement[4]

                # The owner of the table on which the index is created
                self.on_table_owner = splitted_statement[4]

        # The list of the attributes
        attributes_string = get_string_between_tags(index_statement, "(", ")")
        spliited_attributes = attributes_string.split(', ')

        self.attributes_list = []
        for attribute in spliited_attributes:
            self.attributes_list.append(attribute)

        # The chunk on which it is installed
        self.chunk = index_statement.split(' in ')[1][:-1]

    def __eq__(self, other_index):
        """
        Two indexes instances are equal only if all of their fields are equals.
        :param other_index: The other index instance to compare with
        :return: True if the two indexes instances are equal
        """

        return self.index_name == other_index.index_name \
            and self.unique_constraint == other_index.unique_constraint \
            and self.index_owner == other_index.index_owner \
            and self.attributes_list == other_index.attributes_list \
            and self.on_table == other_index.on_table \
            and self.on_table_owner == other_index.on_table_owner \
            and self.chunk == other_index.chunk

# coding=utf-8


class Attribute:
    """
    An attribute is defined by :
        - The table in which it exists
        - The name of the column
        - The data type
        - The column definition
    """

    def __init__(self, table, create_definition):
        """
        We create a new Attribute instance by giving it the table instance (usefull to get the table
        name from the attribute) and the create definition (col_name + data_type + col_definition)
        :param table: The table instance
        :param create_definition: The create definition
        """

        splitted_definition = create_definition.split(' ', 2)

        # Table instance
        self.table = table

        # Column name
        self.col_name = splitted_definition[0]

        # Data type
        self.data_type = splitted_definition[1]

        # Column definition
        if len(splitted_definition) == 3:
            self.col_definition = splitted_definition[2]
        else:
            self.col_definition = ""

    def __eq__(self, other_attribute):
        """
        Two attributes instances are equal only if all of their fields are equals.
        :param other_attribute: The other attribute instance to compare with
        :return: True if the two attributes instances are equal
        """

        return self.col_name == other_attribute.col_name \
            and self.data_type == other_attribute.data_type \
            and self.col_definition == other_attribute.col_definition \
            and self.table.table_name == other_attribute.table.table_name \
            and self.table.database.database_name == other_attribute.table.database.database_name

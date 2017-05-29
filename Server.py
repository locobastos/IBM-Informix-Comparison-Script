# coding=utf-8
from Database import Database


class Server:
    """
    A server is described by :
        - It's name
        - It's dictionnary of databases
    """

    def __init__(self, file):
        """
        We create a new Server instance by giving it the file containing the formatted tbschema
        result.
        :param file: The file containing the tbschema without comment nor multispace nor empty line.
        """

        # Server's name
        self.server_name = file.split('-')[1]

        # Dictionnary of databases
        self.dictionnary_databases = {}
        self.add_database_to_dictionnary(file)

    def add_database_to_dictionnary(self, file):
        """
        Add a database into the dictionnary of the right server
        :param file: file of the databse
        """

        database_name = file.split('-')[2]
        if database_name not in self.dictionnary_databases:
            self.dictionnary_databases[database_name] = Database(self,
                                                                 file_content_to_list(file))


def file_content_to_list(file):
    """
    Append each line of the file to a theèlist
    :param file: The file to transform into a theèlist
    :return: The the list
    """

    lst = []
    with open(file) as file_alias:
        for line in file_alias:
            lst.append(line)
    return lst

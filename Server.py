# coding=utf-8
from Database import Database


class Server:
    """
    A server is described by :
        - It's name
        - It's dictionnary of databases
    """

    def __init__(self, serv_name, database_name, file):
        """
        We create a new Server instance by giving it the file containing the formatted tbschema
        result and the name of the server.
        :param serv_name: The name of the server.
        :param file: The file containing the tbschema without comment nor multispace nor empty line.
        """

        # Server's name
        self.server_name = serv_name

        # Dictionnary of databases
        self.dictionnary_databases = {}
        self.add_database_to_dictionnary(database_name, file)

    def add_database_to_dictionnary(self, database_name, file):
        """
        Add a database into the dictionnary of the right server
        :param database_name: the name of the database
        :param file: file of the databse
        """

        database_name = database_name
        if database_name not in self.dictionnary_databases:
            self.dictionnary_databases[database_name] = Database(self,
                                                                 file_content_to_list(file))

    def __eq__(self, other_server):
        """
        Two server instances are equal only if their dictionnary of databases are equals.
        :param other_server: The other server instance to compare with
        :return: True if the two servers instances are equal
        """

        equal = True

        for database in list(self.dictionnary_databases.keys()):
            db_instance = self.dictionnary_databases.get(database)
            if not db_instance.__eq__(other_server.dictionnary_databases.get(database)):
                equal = False
                break

        return equal


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

# coding=utf-8
from Table import Table
from Index import Index
from Grant import Grant
from Revoke import Revoke


class Database:
    """
    A database is described by :
        - The server on which it is installed
        - Its name
        - Its dictionnary of tables
        - Its dictionnary of indexes
        - Its dictionnary of grants
        - Its dictionnary of revokes
        (- Its dictionnary of views, not implemented yet)
    """

    def __init__(self, server, list):
        """
        We call the Database class by giving it the server object (usefull to get the server name
        from the database) and the list of the content of the tbschema formatted file.
        :param server: The server object
        :param list: The list of the tbschema content
        """

        # Server object
        self.server = server

        # Database's name
        for i in self.get_all_keyword_position_in_list('database ', list):
            self.database_name = list[i].split()[1]

        # Dictionnary of tables
        self.tables_dictionnary = {}
        for i in self.get_all_keyword_position_in_list('create table ', list):
            table_name = self.get_table_name(list[i])
            self.tables_dictionnary[table_name] = Table(self, list[i][:-1])

        # Dictionnary of indexes
        self.indexes_dyctionnary = {}
        for i in self.get_all_keyword_position_in_list('create index ', list):
            index_name = self.get_index_name(list[i], False)
            self.indexes_dyctionnary[index_name] = Index(self, list[i][:-1])

        for i in self.get_all_keyword_position_in_list('create unique index ', list):
            index_name = self.get_index_name(list[i], True)
            self.indexes_dyctionnary[index_name] = Index(self, list[i][:-1])

        # Dictionnary of grants
        self.grants_dictionnary = {}
        for i in self.get_all_keyword_position_in_list('grant ', list):
            grant_key = self.get_grant_key(list[i])
            self.grants_dictionnary[grant_key] = Grant(self, list[i][:-1])

        # Dictionnary of revokes
        self.revokes_dictionnary = {}
        for i in self.get_all_keyword_position_in_list('revoke ', list):
            revoke_key = self.get_revoke_key(list[i])
            self.revokes_dictionnary[revoke_key] = Revoke(self, list[i][:-1])

        # TODO: Implement the views dictionnary
        # Dictionnary of views
        # self.views_dictionnary = {}
        # for i in self.get_all_keyword_position_in_list(liste, 'create view '):
        #     view_name = self.get_views_name(list[i])
        #     self.views_dictionnary[view_name] = View(self, liste[i][:-1]))

    def get_all_keyword_position_in_list(self, keyword, list):
        """
        Return a second list of all indexes of the first list where my keyword appears.
        :param keyword: The keyword to search off
        :param list: The list where we search for the keyword
        :return: The list of all indexes
        """

        results = []
        list_indexes = [i for i, entry in enumerate(list) if keyword in entry]

        for i in list_indexes:
            results.append(i)

        return results

    def get_table_name(self, create_table_statement):
        """
        Return the name of the table from the create table statement.
        :param create_table_statement: The create table statement
        :return: The name of the table
        """

        if "." in create_table_statement.split(' ', 3)[2]:
            table_name = create_table_statement.split(' ', 3)[2].split('.')[1]
        else:
            table_name = create_table_statement.split(' ', 3)[2]

        return table_name

    def get_index_name(self, create_index_statement, unique_constraint):
        """
        Return the name of the index from the create index statement.
        :param create_index_statement: The create index statement
        :param unique_constraint: The unique constraint
        :return: The name of the index
        """

        splitted_statement = create_index_statement.split(' ', 6)

        if unique_constraint:
            if "." in splitted_statement[3]:
                index_name = splitted_statement[3].split('.')[1]
            else:
                index_name = splitted_statement[3]
        else:
            if "." in splitted_statement[2]:
                index_name = splitted_statement[2].split('.')[1]
            else:
                index_name = splitted_statement[2]

        return index_name

    def get_grant_key(self, grant_statement):
        """
        Create the key from the grant statement.
        The key will be used as the dictionnary key.
        :param grant_statement: The grant statement
        :return: The key
        """

        splitted_statement = grant_statement.split()
        grant_privilege = splitted_statement[1]

        if "." in splitted_statement[3]:
            grant_table = splitted_statement[3].split('.')[1]
        else:
            grant_table = splitted_statement[3]

        return grant_privilege + "_" + grant_table

    def get_revoke_key(self, revoke_statement):
        """
        Create the key from the revoke statement.
        The key will be used as the dictionnary key.
        :param revoke_statement: The revoke statement
        :return: The key
        """

        splitted_statement = revoke_statement.split()
        revoke_privilege = splitted_statement[1]

        if "." in splitted_statement[3]:
            revoke_table = splitted_statement[3].split('.')[1]
        else:
            revoke_table = splitted_statement[3]

        return revoke_privilege + "_" + revoke_table

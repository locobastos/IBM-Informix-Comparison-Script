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

    def __init__(self, server, lst):
        """
        We create a new Database instance by giving it the server instance (usefull to get the
        server name from the database) and the list of the content of the tbschema formatted file.
        :param server: The server instance
        :param lst: The list of the tbschema content
        """

        # Server instance
        self.server = server

        # Database's name
        for i in get_all_keyword_position_in_list('database ', lst):
            self.database_name = lst[i].split()[1][:-1]

        # Dictionnary of tables
        self.tables_dictionnary = {}
        for i in get_all_keyword_position_in_list('create table ', lst):
            table_name = get_table_name(lst[i])
            self.tables_dictionnary[table_name] = Table(self, lst[i][:-1])

        # Dictionnary of indexes
        self.indexes_dictionnary = {}
        for i in get_all_keyword_position_in_list('create index ', lst):
            index_name = get_index_name(lst[i], False)
            self.indexes_dictionnary[index_name] = Index(self, lst[i][:-1])

        for i in get_all_keyword_position_in_list('create unique index ', lst):
            index_name = get_index_name(lst[i], True)
            self.indexes_dictionnary[index_name] = Index(self, lst[i][:-1])

        # Dictionnary of grants
        self.grants_dictionnary = {}
        for i in get_all_keyword_position_in_list('grant ', lst):
            grant_key = get_grant_key(lst[i])
            self.grants_dictionnary[grant_key] = Grant(self, lst[i][:-1])

        # Dictionnary of revokes
        self.revokes_dictionnary = {}
        for i in get_all_keyword_position_in_list('revoke ', lst):
            revoke_key = get_revoke_key(lst[i])
            self.revokes_dictionnary[revoke_key] = Revoke(self, lst[i][:-1])

        # TODO: Implement the views dictionnary
        # Dictionnary of views
        # self.views_dictionnary = {}
        # for i in self.get_all_keyword_position_in_list(liste, 'create view '):
        #     view_name = self.get_views_name(list[i])
        #     self.views_dictionnary[view_name] = View(self, liste[i][:-1]))

    def __eq__(self, other_database):
        """
        Two databases instances are equal only if all of their fields are equals.
        :param other_database: The other database instance to compare with
        :return: True if the two databases instances are equal
        """

        attr_equal = self.database_name == other_database.database_name
        tbl_equal = True
        idx_equal = True
        grt_equal = True
        rvk_equal = True

        if attr_equal:
            for table in list(self.tables_dictionnary.keys()):
                tbl_instance = self.tables_dictionnary.get(table)
                if not tbl_instance.__eq__(other_database.tables_dictionnary.get(table)):
                    tbl_equal = False
                    break

        if attr_equal and tbl_equal:
            for index in list(self.indexes_dictionnary.keys()):
                idx_instance = self.indexes_dictionnary.get(index)
                if not idx_instance.__eq__(other_database.indexes_dyctionnary.get(index)):
                    idx_equal = False
                    break

        if attr_equal and tbl_equal and idx_equal:
            for grant in list(self.grants_dictionnary.keys()):
                grt_instance = self.grants_dictionnary.get(grant)
                if not grt_instance.__eq__(other_database.grants_dyctionnary.get(grant)):
                    grt_equal = False
                    break

        if attr_equal and tbl_equal and idx_equal and grt_equal:
            for revoke in list(self.revokes_dictionnary.keys()):
                rvk_instance = self.revokes_dictionnary.get(revoke)
                if not rvk_instance.__eq__(other_database.revokes_dictionnary.get(revoke)):
                    rvk_equal = False
                    break

        return attr_equal and tbl_equal and idx_equal and grt_equal and rvk_equal


def get_all_keyword_position_in_list(keyword, lst):
    """
    Return a second list of all indexes of the first list where my keyword appears.
    :param keyword: The keyword to search off
    :param lst: The list where we search for the keyword
    :return: The list of all indexes
    """

    results = []
    list_indexes = [i for i, entry in enumerate(lst) if keyword in entry]

    for i in list_indexes:
        results.append(i)

    return results


def get_table_name(create_table_statement):
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


def get_index_name(create_index_statement, unique_constraint):
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


def get_grant_key(grant_statement):
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


def get_revoke_key(revoke_statement):
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

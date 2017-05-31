# coding=utf-8


class Revoke:
    """
    A revoke is described by :
        - The database on which it exists
        - The privilege revoked
        - The user on wich the revoke applies
        - The table on which the revoke applies
        - The owner of the table on which the revoke applies
    """

    def __init__(self, database, revoke_statement):
        """
        We create a new Revoke instance by giving it the database instance (usefull to get the
        database name from the revoke statement) and the revoke statement.
        :param database: The database instance
        :param revoke_statement: The revoke statement
        """

        splitted_statement = revoke_statement.split()

        # Database statement
        self.database = database

        # Privilege revoked
        self.privilege_revoked = splitted_statement[1]

        # The user on which the revoke applies
        self.user_revoked = splitted_statement[-1][:-1]

        if "." in splitted_statement[3]:
            # The table on which the revoke applies
            self.table_revoke = splitted_statement[3].split('.')[1]

            # The owner of the table on which the revoke applies
            self.table_owner_revoke = splitted_statement[3].split('.')[0]
        else:
            # The table on which the revoke applies
            self.table_revoke = splitted_statement[3]

            # The owner of the table on which the revoke applies
            self.table_owner_revoke = splitted_statement[3]

    def __eq__(self, other_revoke):
        """
        Two revokes instances are equal only if all of their fields are equals.
        :param other_revoke: The other revoke instance to compare with
        :return: True if the two revokes instances are equal
        """

        return self.privilege_revoked == other_revoke.privilege_revoked \
            and self.user_revoked == other_revoke.user_revoked \
            and self.table_revoke == other_revoke.table_revoke \
            and self.table_owner_revoke == other_revoke.table_owner_revoke \
            and self.database.database_name == other_revoke.database.database_name

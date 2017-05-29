# coding=utf-8


class Grant:
    """
    A grant is described by :
        - The database on which it exists
        - The privilege granted
        - The table on which the grant applies
        - The owner of the table on which the grant applies (OPTIONNAL)
        - The user on wich the grant applies
        - The user's alias
    """

    def __init__(self, database, grant_statement):
        """
        We create a new Grant instance by giving it the database instance (usefull to get the
        database name from the grant statement) and the grant statement.
        :param database: The database instance
        :param grant_statement: The grant statement
        """

        splitted_statement = grant_statement.split()

        # Database statement
        self.database = database

        # Privilege granted
        self.privilege_granted = splitted_statement[1]

        if len(splitted_statement) > 4:
            # Example : grant select on "informix".table_a to public as "informix"

            if "." in splitted_statement[3]:
                # The table on which the grant applies
                self.table_grant = splitted_statement[3].split('.')[1]

                # The owner of the table on which the grant applies
                self.table_owner_grant = splitted_statement[3].split('.')[0]
            else:
                # The table on which the grant applies
                self.table_grant = splitted_statement[3]

                # The owner of the table on which the grant applies
                self.table_owner_grant = splitted_statement[3]

            # The user on wich the grant applies
            self.user_granted = splitted_statement[5]

            # The user's alias
            self.user_alias_granted = splitted_statement[7]
        else:
            # Example : grant connect to public

            self.table_grant = ""
            self.table_owner_grant = ""
            self.user_granted = ""
            self.user_alias_granted = ""

    def __eq__(self, other_grant):
        """
        Two grants instances are equal only if all of their fields are equals.
        :param other_grant: The other grant instance to compare with
        :return: True if the two grants instances are equal
        """

        return self.privilege_granted == other_grant.privilege_granted \
            and self.table_grant == other_grant.table_grant \
            and self.table_owner_grant == other_grant.table_owner_grant \
            and self.user_granted == other_grant.user_granted \
            and self.user_alias_granted == other_grant.user_alias_granted

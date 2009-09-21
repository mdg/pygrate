import pygration


class AccountTable(pygration.Step):
    """Creates an account table."""

    def add( self, db ):
        db.sql("CREATE TABLE account (id integer, balance integer);")


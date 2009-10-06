import pygration


@pygration.step_class
class AccountTable(object):
    """Creates an account table."""

    def add( self, db ):
        db.sql("CREATE TABLE account (id integer, balance integer);")


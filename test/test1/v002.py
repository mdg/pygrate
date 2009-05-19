import pygrate


class AccountTable(pygrate.Pygration):
    """Creates an account table."""

    table = pygrate.Table( "account",
            [ pygrate.Integer("id")
            , pygrate.Integer("balance")
            ])

    def add( self, db ):
        db.create(table)


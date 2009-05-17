import pygrate


class EmployeeTable(pygrate.Pygration):
    """Creates an employee table."""

    table = pygrate.Table( "employee",
            [ pygrate.Number("id")
            , pygrate.Number("name")
            ])

    def add( self, db ):
        db.create(table)


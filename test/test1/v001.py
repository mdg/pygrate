import pygrate


employee_table = """
employee:
    id: integer
"""


class SalaryTable(pygrate.Pygration):
    """Creates a salary table."""

    table = pygrate.Table( "employee",
            [ pygrate.Integer("id")
            , pygrate.Integer("employee")
            , pygrate.Integer("year")
            , pygrate.Integer("salary")
            ])

    def add( self, db ):
        db.create(table)


class EmployeeTable(pygrate.Pygration):
    """Creates an employee table."""

    table = pygrate.Table( "employee",
            [ pygrate.Integer("id")
            , pygrate.String("name")
            ])

    def add( self, db ):
        db.create(table)


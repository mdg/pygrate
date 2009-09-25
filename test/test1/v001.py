import pygration


class SalaryTable(pygration.Step):
    """Creates a salary table."""

    def add( self, db ):
        db.sql("CREATE TABLE salary;")


class EmployeeTable(pygration.Step):
    """Creates an employee table."""

    def add( self, db ):
        db.sql("CREATE TABLE employee;")


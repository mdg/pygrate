import pygration


@pygration.step_class
class SalaryTable(object):
    """Creates a salary table."""

    def add( self, db ):
        db.sql("CREATE TABLE salary;")


@pygration.step_class
class EmployeeTable(object):
    """Creates an employee table."""

    def add( self, db ):
        db.sql("CREATE TABLE employee;")


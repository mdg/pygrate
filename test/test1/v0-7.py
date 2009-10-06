import pygration


@pygration.step_class
class EmployeeTable(object):
    def add( self, db ):
        db.sql( \
                """
                CREATE TABLE employee2
                ( id number
                , txt_val varchar2(79)
                );
                """ )

    def drop( self, db ):
        db.sql('DROP TABLE old_employee')



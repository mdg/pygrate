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

@pygration.step_class
class EmployeeValueIndex(object):
    def add(self, db):
        db.sql("CREATE INDEX employee2idx ON employee2.txt_val;")

    def rollback_add(self, db):
        db.sql("DROP INDEX employee2idx;")


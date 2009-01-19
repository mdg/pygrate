import pygrate


class CreateEmployeeTable(pygrate.Pygration):
    def add( self, db ):
        print "sample add"
        db.drop_table( "employee" )
        db.execute_sql(
                """
                CREATE TABLE employee
                ( a number
                , b varchar2(10)
                );""" )

class CreateJobTable(pygrate.Pygration):
    def add( self, db ):
        db.execute_sql( \
                """
                CREATE TABLE job
                ( id number
                , name varchar2(57)
                );
                """ )

    def drop( self, db ):
        db.drop_table('job')

    def execute_sql( self, sql ):
        print "executed on the db:\n%s\n" % ( sql )

class DropSuperTable(pygrate.Pygration):
    def hide(self,db):
        print "sample hide"
        db.hide_table("super")

    def drop(self,db):
        print "sample drop"
        db.drop_table("super")



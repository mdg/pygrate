import pygrate


class CreateEmployeeTable(pygrate.Pygration):
    def __init__( self ):
        self._sql = \
                """
                CREATE TABLE employee
                ( a number
                , b varchar2(10)
                );
                """

class CreateJobTable(pygrate.Pygration):
    def pre_up( self, step ):
        step.execute_sql( \
                """
                CREATE TABLE job
                ( id number
                , name varchar2(20)
                );
                """ )

    def pre_down( self, step ):
        step.execute_sql( "DROP TABLE job" );

    def execute_sql( self, sql ):
        print "executed on the db:\n%s\n" % ( sql )



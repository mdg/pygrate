import pygrate


class CreateEmployeeTable(pygrate.Pygration):
    def add( self, db ):
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
        db.hide_table("super")

    def drop(self,db):
        db.drop_table("super")


class RenameUserIDColumn(pygrate.Pygration):
    """Rename the userid column to be username."""
    def add(self,db):
        """Add the username column and copy userid values to it."""
        db.add_column( "user", String( "username") )
        db.execute_sql( "update user set username=userid;" )

    def hide(self,db):
        """Hide the userid column before completely dropping it."""
        db.hide_column( "user.userid" )

    def drop(self,db):
        """Permanently drop the userid column."""
        db.drop_column( "user.userid" )


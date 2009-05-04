from pygrate import pygration
from pygrate.pygration import Pygration


class CreateEmployeeTable(pygration.Pygration):
    def __init__( self, db ):
        db.execute_sql( \
                """
                CREATE TABLE employee
                ( id number
                , first_name varchar2(20)
                , last_name varchar2(20)
                );
                """ )


class CreateJobTable(pygration.Pygration):
    def add( self, db ):
        db.execute_sql( \
                """
                CREATE TABLE job
                ( id number
                , name varchar2(20)
                );
                """ )

    def rollback_add( self, db ):
        db.execute_sql( "DROP TABLE job;" );

    def execute_sql( self, sql ):
        print "executed on the db:\n%s\n" % ( sql )


class CreateOfficeTable(pygrate.Pygration):
    """Add a new table to store office information."""

    office_table = pygrate.Table( "office", \
            [ pygrate.Number( "id" )
            , pygrate.String( "city" )
            ] )

    def add( self, db ):
        db.create( office_table )
        db.add( office_table )
        db.create_table( "office", \
                [ pygration.Number( "id" )
                , pygration.String( "city" )
                ] )
        db.table( "employee" ).add_column( Number( "office" ) )
        db.add_column( "employee", pygration.Number( "office" ) )

    def rollback_add( self, db ):
        db.rollback_add( office_table )


class DropOfficeTable(pygrate.Pygration):
    """Remove the office table."""

    office_table = pygrate.Table( "office" )

    def hide( self, db ):
        db.hide( office_table )
        db.hide_column( "employee.office" )
        db.hide_table( "employee" )

    def drop( self, db ):
        db.drop( office_table )
        db.drop_column( "employee.office" )
        db.drop_table( "employee" )

    def rollback_hide( self, db ):
        db.rollback_hide( office_table )


class DropOldColumn(pygration.Pygration):
    def hide( self, db ):
        db.hide_column( "employee.old_column" )

    def drop( self, db ):
        db.drop_column( "employee.old_column" )

    def rollback_hide( self, db ):
        db.unhide_column( "employee.old_column" )


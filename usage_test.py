from pygrate.pygration import Pygration


class CreateEmployeeTable(Pygration):
    def __init__( self, db ):
        db.execute_sql( \
                """
                CREATE TABLE employee
                ( id number
                , first_name varchar2(20)
                , last_name varchar2(20)
                );
                """ )


class CreateJobTable(Pygration):
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


class CreateOfficeTable(Pygration):
    def add( self, db ):
        db.create_table( "office", \
                [ Number( "id" )
                , String( "city" )
                ] )
        db.table( "employee" ).add_column( Number( "office" ) )
        db.add_column( "employee", pygration.Number( "office" ) )

    def hide( self, db ):
        db.hide_column( "employee.office" )
        db.hide_table( "employee" )

    def drop( self, db ):
        db.drop_column( "employee.office" )
        db.drop_table( "employee" )

    def rollback_add( self, db ):
        pass

    def rollback_hide( self, db ):
        pass


class DropOldColumn(Pygration):
    def hide( self, db ):
        db.hide_column( "employee.old_column" )

    def drop( self, db ):
        db.drop_column( "employee.old_column" )

    def rollback_hide( self, db ):
        db.unhide_column( "employee.old_column" )


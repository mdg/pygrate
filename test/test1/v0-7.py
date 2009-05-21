from pygrate.pygration import Pygration


class EmployeeTable(Pygration):
    def add( self, db ):
        db.execute_sql( \
                """
                CREATE TABLE txt
                ( id number
                , txt_val varchar2(79)
                );
                """ )

    def hide( self, db ):
        db.hide_table( 'txt' )

    def drop( self, db ):
        db.drop_table( 'txt' )



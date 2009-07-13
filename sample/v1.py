import pygration


class CreateEmployeeTable(pygration.Step):
    def add(self, db):
        db.execute_sql(
                """
                CREATE TABLE employee
                ( a number
                , b varchar2(10)
                );""" )


class CreateJobTable(pygration.Step):
    def add(self, db):
        db.execute_sql( \
                """
                CREATE TABLE job
                ( id number
                , name varchar2(57)
                );
                """ )


class RenameEmployeeNumberColumn(pygration.Step):
    """Rename the userid column to be username."""
    def add(self,db):
        """Add the username column and copy userid values to it."""
        db.execute_sql( "ALTER TABLE employee ADD COLUMN id number" )
        db.execute_sql( "update user set id=number;" )
        # create trigger to update the new username column

    def hide(self,db):
        """Hide the userid column before completely dropping it."""
        db.sql( "ALTER TABLE employee RENAME COLUMN number pd_number" )

    def drop(self,db):
        """Permanently drop the userid column."""
        db.sql("ALTER TABLE employee DROP COLUMN pd_number")


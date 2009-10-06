import pygration


@pygration.step_class
class CreateEmployeeTable(object):
    ID = "1"

    def add(self, db):
        db.sql(
                """
                CREATE TABLE employee
                ( id number
                , firstname varchar2(10)
                , lastname varchar2(10)
                );""" )

    def rollback_add(self, db):
        db.sql("DROP TABLE employee;")


class CreateJobTable(object):
    ID = "2"

    def add(self, db):
        db.sql( \
                """
                CREATE TABLE job
                ( id number
                , name varchar2(57)
                );
                """ )

    def rollback_add(self, db):
        db.sql("DROP TABLE job;")

pygration.step_instance(CreateJobTable())


import pygration


class CreateSalaryTable(pygration.Step):
    def add(self, db):
        db.sql( """
                CREATE TABLE salary
                ( employee number
                , salary number
                );""" )


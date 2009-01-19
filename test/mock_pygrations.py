from pygrate.pygration import Pygration
from pygrate import pygration


class CreateUserTable(Pygration):
    def add(self,db):
        columns = [pygration.Number("id"),pygration.String("username")]
        db.create_table("user",columns)


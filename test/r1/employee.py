from pygrate.pygration import Pygration


class EmployeeTable(Pygration):
    def add( self, db ):
        print "EmployeeTable.add()"

    def hide( self, db ):
        print "EmployeeTable.hide()"

    def drop( self, db ):
        print "EmployeeTable.drop()"


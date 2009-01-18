import pygration
import optparse
import os.path
import sys
import inspect
import types


class PygrationDB:
    """A single step for a migration.
    """

    def execute_sql( self, sql ):
        self._sql = sql

    def execute_sql_file( self, sql_file ):
        self._sql_file = sql_file

class AddPygrationDB(PygrationDB):
    """Adds elements to the DB.
    """

    def add_column( self, table, column ):
        pass

class HidePygrationDB(PygrationDB):
    """Hides elements in the DB prior to being dropped.
    """

    def hide_column( self, table_column ):
        pass

class DropPygrationDB(PygrationDB):
    """Drops elements from the DB.
    """

    def drop_column( self, table_column ):
        pass

class RollbackHidePygrationDB(PygrationDB):
    pass

class RollbackDropPygrationDB(PygrationDB):
    pass


class Pygrator:
    """The operator for running a set of pygrations.
    """

    def __init__( self, path, migration ):
        self._path = path
        self._migration = migration
        self._modules = []
        self._import_migrations()
        # iterate through each module
        # create each migration
        self._migrations = self._create_migrations()

    def migrate( self, stage ):
        db = self._create_db( stage )
        # execute the given stage of each migration
        # self._migrate( stage, db, migrations )

    def _create_migrations( self ):
        migs = []
        for mod in self._modules:
            print "module: "+ str(mod) + "\n"
            for mig in mod.__dict__.values():
                # if isinstance(mig, pygration.Pygration):
                if self._pygration_subclass(mig):
                    # print "was instance"
                    print "mig: "+ str(mig.__name__)
                    migs.append(mig())
        return migs

    def _create_db( self, stage ):
        """Create the PygrationDB for the given stage"""
        db = None
        if stage == 'add':
            db = AddPygrationDB()
        elif stage == 'hide':
            db = HidePygrationDB()
        elif stage == 'drop':
            db = DropPygrationDB()
        elif stage == 'rollback_add':
            db = RollbackAddPygrationDB()
        elif stage == 'rollback_hide':
            db = RollbackDropPygrationDB()
        else:
            pass # throw an exception here
        return db

    def _import_migrations( self ):
        migrations = self._list_migrations()
        modules = []
        sys.path.insert( 0, os.path.abspath( self._path ) )
        for m in migrations:
            print "__import__( "+ str(os.path.join( self._migration, m ) ) +")"
            mod = __import__( os.path.join( self._migration, m ) )
            modules.append( mod )
        self._modules = modules

        # mod_name = os.path.join( self._path, self._migration )
        # print "mod_name = "+ str(mod_name)
        # mod = __import__( mod_name )
        # print str(dir(mod))

    def _list_migrations( self ):
        migration_path = os.path.join( self._path, self._migration )
        print "migration_path = "+ str(migration_path)
        files = os.listdir( migration_path )
        migrations = []
        for f in files:
            if f.endswith( '.py' ):
                migrations.append( f.replace( ".py", "" ) )
        # print str(migrations)
        return migrations

    def _pygration_subclass( self, obj ):
        if type(obj) is not types.ClassType:
            return False
        return issubclass(obj, pygration.Pygration) \
                and not obj == pygration.Pygration


def run_main():
    usage = "usage: %prog [options] stage migration"
    parser = optparse.OptionParser( usage=usage )
    parser.add_option( "-p", "--path" )

    opts, args = parser.parse_args()
    # print opts
    # print args

    if len(args) == 0:
        parser.error("A stage must be specified")
    if len(args) == 1:
        parser.error("A migration set must be specified")
    if len(args) > 2:
        parser.error("Too many arguments")

    stage = args[0]
    migration = args[1]

    path = '.'
    if opts.path:
        print "opts.path="+ opts.path
        path = opts.path

    p = Pygrator( path, migration )
    p.migrate( stage )


if ( __name__ == "__main__" ):
    run_main()


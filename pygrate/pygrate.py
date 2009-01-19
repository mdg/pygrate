import pygration
import pygration_db
import database
import os.path
import sys
import inspect
import types


class Pygrator:
    """The operator for running a set of pygrations.
    """
    # MIGRATOR_MAP = { 'add': 

    def __init__( self, db, path, migration ):
        self._db = db
        self._path = path
        self._migration = migration
        self._modules = []
        self._import_migrations()
        # iterate through each module
        # create each migration
        self._migrations = self._create_migrations()

    def migrate( self, stage ):
        pygration_db = self._create_db( stage )
        self._migrate( stage, pygration_db )

    def _create_migrations( self ):
        migs = []
        for mod in self._modules:
            print "module: "+ str(mod) + "\n"
            for mig in mod.__dict__.values():
                if self._pygration_subclass(mig):
                    # print "was instance"
                    print "mig: "+ str(mig.__name__)
                    migs.append(mig())
        return migs

    def _migrate( self, stage, pdb ):
        for m in self._migrations:
            if stage == 'add':
                m.add( pdb )
            elif stage == 'hide':
                m.hide( pdb )

    def _create_db( self, stage ):
        """Create the PygrationDB for the given stage"""
        pdb = pygration_db.PygrationDB( self._db )
        return pdb

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


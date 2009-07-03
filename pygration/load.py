import pygration
from step import StepType
import os.path
import sys
import imp
import inspect
import types


class VersionFinder(object):
    """Object for finding available pygration_sets."""
    def __init__(self, path):
        self._path = path
        self._versions = []

    def find_versions( self ):
        #print "_find_versions"
        files = os.listdir( self._path )
        versions = []
        for f in files:
            p = os.path.join(self._path, f)
            if not os.path.isfile(p):
                continue
            #print "f = %s" % f
            root, ext = os.path.splitext(f)
            if ext != ".py":
                continue
            #print "root, ext = %s, %s" % (root, ext)
            v = Version( root )
            if v.is_pygration():
                versions.append(v)
        versions.sort()
        return versions


class VersionSetLoader:
    """Loads a given set of Pygrations at runtime."""

    def __init__(self, path, version):
        self._path = path
        self._version = version
        self._steps = []
        self._pygrations = []

    def load(self):
        return self._import_module()

    def steps(self):
        return self._steps

    def pygrations(self):
        return self._pygrations

    def _import_module(self):
        """Import the module & pygrations for the given version.

        Also creates pygrations from that module and does so in the
        order they are written in the file.
        """

        # pygrations should be passed in as an array, not called directly here
        initial_count = len(StepType.pygrations)
        module_name = os.path.join( self._version )
        print "pygration_path = "+ str(module_name)

        sys.path.insert( 0, os.path.abspath( self._path ) )
        mod_trip = imp.find_module(module_name)
        mod = imp.load_module(module_name, *mod_trip)
        self._modules.append( mod )
        # need to close the file in mod_trip

        pygration_classes = StepType.pygrations[initial_count:]
        pygrations = []
        for pcls in pygration_classes:
            pygrations.append( pcls() )
        self._pygrations = pygrations
        return self._pygrations

def select_config(conf_files, env):
    if len(conf_files) == 1:
        print "select single config file"
        return conf_files[0]
    for c in conf_files:
        if c.find(env) == 0:
            pass
    return None


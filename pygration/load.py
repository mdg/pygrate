import pygration
from step import StepType
import os.path
import sys
import imp
import inspect
import types


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


import yaml
from yaml import Loader, Dumper


class Config:
    """Config parsing file."""

    def __init__(self):
        self.schema = None
        self.connection = None
        self.opts = {}

    def load(self, conf_file):
        self.opts = yaml.load(conf_file)
        print "opts = %s" % repr(self.opts)
        if self.opts:
            self._set_option('schema')
            self._set_option('connection')
        else:
            self.opts = {}

    def _set_option(self, option):
        if self.opts and option in self.opts:
            setattr(self, option, self.opts[option])

    def __repr__(self):
        return "<Config(%s)>" % self.opts


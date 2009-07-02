import yaml
from yaml import Loader, Dumper


class Config:
    """Config parsing file."""

    def __init__(self):
        self.schema = None
        self.connection = None
        self.db_opts = {}

    def load(self, conf_file):
        self.db_opts = yaml.load(conf_file)
        print "db_opts = %s" % repr(self.db_opts)
        if self.db_opts:
            self._set_option('schema')
            self._set_option('connection')
        else:
            self.db_opts = {}

    def _set_option(self, option):
        if self.db_opts and option in self.db_opts:
            setattr(self, option, self.db_opts[option])


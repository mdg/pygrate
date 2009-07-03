import yaml
from yaml import Loader, Dumper


class Config:
    """Config file loader
    
    Parses yaml content into config options."""

    def __init__(self):
        self.schema = None
        self.connection = None
        self.username = None
        self.password = None
        self.opts = {}

    def load(self, conf_file):
        self.opts = yaml.load(conf_file)
        if self.opts:
            self._set_option('connection')
            self._set_option('schema')
            self._set_option('username')
            self._set_option('password')
        else:
            self.opts = {}

    def _set_option(self, option):
        if self.opts and option in self.opts:
            setattr(self, option, self.opts[option])

    def __str__(self):
        return str(self.opts)

    def __repr__(self):
        return "<Config(%s)>" % self.opts


def select(conf_files, env):
    """Select a config file that matches the given environment.

    Default to the single config file if only 1 and no environment given.
    """
    if len(conf_files) == 1 and env is None:
        return conf_files[0]
    for c in conf_files:
        if c.find(env) == 0:
            pass
    return None


def load(conf_filename):
    f = open(conf_filename)
    c = Config()
    c.load(f)
    return c


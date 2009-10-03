import yaml
from yaml import Loader, Dumper


class Config:
    """Config file loader
    
    Parses yaml content into config options."""

    def __init__(self):
        self.opts = {}

    def load(self, conf_file):
        self.opts = yaml.load(conf_file)

    def __getattr__(self, name):
        return self.opts.get(name, None)

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
        name, sep, extension = c.rpartition('.')
        if name == env and extension == 'yaml':
            return c
    return None


def load(conf_filename):
    f = open(conf_filename)
    c = Config()
    c.load(f)
    return c


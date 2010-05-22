import yaml
from yaml import Loader, Dumper


class Config:
    """Config file loader
    
    Parses yaml content into config options."""

    def __init__(self):
        self.opts = {}

    def load(self, conf_file):
        self.opts = yaml.load(conf_file) or {}

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
    conf_file_map = {}
    for conf_file in conf_files:
        name, sep, extension = conf_file.rpartition('.')
        if extension == 'yaml':
            conf_file_map[name] = conf_file

    if len(conf_file_map) == 1 and env is None:
        name, file = conf_file_map.popitem()
        return file

    return conf_file_map.get(env, None)


def load(conf_filename):
    f = open(conf_filename)
    c = Config()
    c.load(f)
    return c


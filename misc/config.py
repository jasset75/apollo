import os
import yaml
from . dictutils import DictWrapper

settings = None
file = 'project.yml'

if not os.path.isfile(file):
    raise Exception("""
        {} config file not found.
        Please set up this config at your project root folder.
    """.format(file).strip())


class Settings(DictWrapper):

    def __str__(self):
        return str(self)

    def print(self):
        print('-- Settings ----')
        print(yaml.dump(self._dict, default_flow_style=False))
        print('-------------------')


with open(file, 'r') as ymlfile:
    settings = Settings(yaml.load(ymlfile))

# this function prints the configuration file contents

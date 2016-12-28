"""
SW tutorial
~~~~~~~~~~~

Read configuration from a YAML file.
"""

import yaml


def db_connection_string(settings):
    """Return the database connection string
    """
    conn = 'postgresql+psycopg2://'
    if settings.get('DATABASE_USER'):
        conn += settings.get('DATABASE_USER')
        if settings.get('DATABASE_PASSWORD'):
            conn += ':' + settings.get('DATABASE_PASSWORD')
        conn += '@'
    conn += settings.get('DATABASE_HOST') or 'localhost'
    if settings.get('DATABASE_PORT'):
        conn += ':' + str(settings.get('DATABASE_PORT'))
    conn += '/{}'.format(settings.get('DATABASE_DB')
                         or settings.get('DATABASE_USER'))
    return conn


class ConfigLoader(dict):
    """Read a yaml configuration file and build a dictionary from its entries
    """

    def __init__(self, filename=None, defaults=None):
        dict.__init__(self, defaults or {})
        self.load_from_file(filename)

    def load_from_file(self, filename):
        """Read configuration from a YAML file and merge it into global conf
        """
        if filename is None:
            return

        with open(filename, 'r') as stream:
            try:
                conf = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print exc

        conf = self.flatten_dict(conf)
        self.update(conf)

    def flatten_dict(self, raw, prefix=None):
        """Flatten a multi level dictionary and concat its keys

        Example, given the dictionary {'a': {'b': {'c': 1}}}, the function will
        return {'A_B_C': 1}

        """
        acc = {}
        for key, value in raw.iteritems():
            new_key = key.upper()
            if prefix is not None:
                new_key = '_'.join((prefix.upper(), new_key))
            if isinstance(value, dict):
                acc.update(self.flatten_dict(value, new_key))
            else:
                acc[new_key] = value
        return acc

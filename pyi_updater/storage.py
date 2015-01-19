import logging
import os
import shelve

from pyi_updater import settings


log = logging.getLogger(__name__)


class Storage(object):

    def __init__(self, config_dir):
        """Loads & saves config file to file-system

            Args:

                config_dir (str): Path to directory where config will be stored
        """
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.filename = os.path.join(config_dir, settings.CONFIG_FILE_USER)
        log.debug('Config db path: {}'.format(self.filename))

    def save(self, key, value):
        """Saves key & value to database

        Args:

            key (str): used to retrieve value from database

            value (obj): python object to store in database

        """
        db = shelve.open(self.filename)
        db[key] = value
        db.close()

    def load(self, key):
        """Loads value for given key

            Args:

                key (str): The key associated with the value you want
                form the database.

            Returns:

                Object if exists or else None
        """
        db = shelve.open(self.filename)
        value = db.get(key)
        db.close()
        return value

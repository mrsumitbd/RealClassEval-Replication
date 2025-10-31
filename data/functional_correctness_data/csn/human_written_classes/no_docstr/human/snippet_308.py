from fusesoc.provider.provider import get_provider
import os

class Library:

    def __init__(self, name, location, sync_type=None, sync_uri=None, sync_version=None, auto_sync=True):
        if sync_type and (not sync_type in ['local', 'git']):
            raise ValueError("Library {} ({}) Invalid sync-type '{}'".format(name, location, sync_type))
        if sync_type in ['git']:
            if not sync_uri:
                raise ValueError("Library {} ({}) sync-uri must be set when using sync_type 'git'".format(name, location))
        self.name = name
        self.location = location
        self.sync_type = sync_type or 'local'
        self.sync_uri = sync_uri
        self.sync_version = sync_version
        self.auto_sync = auto_sync

    def update(self, force=False):

        def l(s):
            return self.name + ' : ' + s
        if self.sync_type == 'local':
            logger.info(l('sync-type is local. Ignoring update'))
            return
        if not (self.auto_sync or force):
            logger.info(l('auto-sync disabled. Ignoring update'))
            return
        provider = get_provider(self.sync_type)
        if not os.path.exists(self.location):
            logger.info(l(f'{self.location} does not exist. Trying a checkout'))
            try:
                provider.init_library(self)
            except RuntimeError as e:
                logger.warning(l(f'{self.location} does not exist. Ignoring update'))
            return
        try:
            logger.info(l('Updating...'))
            provider.update_library(self)
        except RuntimeError as e:
            logger.error(l('Failed to update library: ' + str(e)))
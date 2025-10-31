import json
import time
import requests

class ElasticItemsWriter:

    def __init__(self, idx_url, clean=False):
        self.idx_url = idx_url
        was_created = self.create_index(self.idx_url, clean=clean)
        if was_created:
            self.create_mapping(idx_url, NOT_ANALYZED_STRINGS_MAPPING)
            self.create_mapping(idx_url, DISABLE_DYNAMIC_MAPPING)

    def write(self, items, max_items=100):
        url = self.idx_url + '/items/_bulk?refresh=true'
        nitems = 0
        bulk_size = 0
        bulk = ''
        packages = []
        for item in items:
            if bulk_size >= max_items:
                packages.append((bulk, bulk_size))
                nitems += bulk_size
                bulk = ''
                bulk_size = 0
            item_json = '{"index" : {"_id" : "%s" } }\n' % item['uuid']
            item_json += json.dumps(item) + '\n'
            bulk += item_json
            bulk_size += 1
        if bulk_size > 0:
            packages.append((bulk, bulk_size))
            nitems += bulk_size
        if packages:
            logger.debug('Writting %i items to %s (%i packs of %i items max)', nitems, url, len(packages), max_items)
        for bulk, nitems in packages:
            task_init = time.time()
            try:
                response = requests.put(url, data=bulk, headers=HEADERS, verify=False)
                response.raise_for_status()
            except UnicodeEncodeError:
                logger.error('Encondig error ... converting bulk to iso-8859-1')
                bulk = bulk.encode('iso-8859-1', 'ignore')
                response = requests.put(url, data=bulk, headers=HEADERS, verify=False)
                response.raise_for_status()
            result = response.json()
            if result['errors']:
                failed_items = [item['index'] for item in result['items'] if 'error' in item['index']]
                error = str(failed_items[0]['error'])
                logger.error('Failed to insert data to ES: %s, %s', error, url)
            logger.debug('Bulk package sent (%.2f sec prev, %i total)', time.time() - task_init, nitems)

    @staticmethod
    def create_index(idx_url, clean=False):
        """Configure the index to work with"""
        try:
            r = requests.get(idx_url, verify=False)
        except requests.exceptions.ConnectionError:
            cause = 'Error connecting to Elastic Search (index: %s)' % idx_url
            raise ElasticSearchError(cause=cause)
        if r.status_code != 200:
            r = requests.put(idx_url, verify=False)
            if r.status_code != 200:
                logger.info("Can't create index %s (%s)", idx_url, r.status_code)
                cause = 'Error creating Elastic Search index %s' % idx_url
                raise ElasticSearchError(cause=cause)
            logger.info('Index %s created', idx_url)
            return True
        elif r.status_code == 200 and clean:
            requests.delete(idx_url, verify=False)
            requests.put(idx_url, verify=False)
            logger.info('Index deleted and created (index: %s)', idx_url)
            return True
        return False

    @staticmethod
    def create_mapping(idx_url, mapping):
        """Create a mapping"""
        mapping_url = idx_url + '/items/_mapping'
        mapping = json.dumps(mapping)
        try:
            r = requests.put(mapping_url, data=mapping, headers=HEADERS, verify=False)
        except requests.exceptions.ConnectionError:
            cause = 'Error connecting to Elastic Search (index: %s, url: %s)' % (idx_url, mapping_url)
            raise ElasticSearchError(cause=cause)
        if r.status_code != 200:
            reason = r.json()['error']
            logger.info("Can't create mapping in %s. %s", mapping_url, reason)
            cause = 'Error creating Elastic Search mapping %s. %s' % (mapping_url, reason)
            raise ElasticSearchError(cause=cause)
        else:
            logger.info('Mapping created in %s', mapping_url)
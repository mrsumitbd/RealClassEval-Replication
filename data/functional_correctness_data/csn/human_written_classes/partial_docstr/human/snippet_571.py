class SimpleGeolocatorCache:
    """Very basic on-disk address -> (lat, lon) cache, using Python's sqlite
    database for on-disk persistence.

    Offers very reasonable performance compared to online lookups.
    """

    def __init__(self, file_name):
        self.connection = conn = sqlite3.connect(file_name)
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS geopy ( address STRING PRIMARY KEY, latitude real, longitude real )')
        self.connection.commit()

    def cached_address(self, address):
        cursor = self.connection.cursor()
        cursor.execute('SELECT latitude, longitude FROM geopy WHERE address=?', (address,))
        res = cursor.fetchone()
        if res is None:
            return None
        return res

    def cache_address(self, address, latitude, longitude):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO geopy(address, latitude, longitude) VALUES(?, ?, ?)', (address, latitude, longitude))
        self.connection.commit()
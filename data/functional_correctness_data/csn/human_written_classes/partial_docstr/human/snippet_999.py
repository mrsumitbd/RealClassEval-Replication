import pkgutil
import random
import csv
import bisect

class Distribution:
    """Creates a random value generator with a weighted distribution
    """

    def __init__(self, resource_name: str) -> None:
        self.total = 0
        self.indices = []
        self.values = []
        self.load_csv_data(resource_name)
        self.length = len(self.values)
        if not self.length:
            raise ValueError('Distribution table must have a record.')

    def load_csv_data(self, resource_name: str) -> None:
        """ Loads the first two columns of the specified CSV file from package data.
        The first column represents the value and the second column represents the count in the population.
        """
        data_bytes = pkgutil.get_data('clkhash', f'{resource_name}')
        if not data_bytes:
            raise ValueError(f'No data resource found with name {resource_name}')
        data = data_bytes.decode('utf8')
        reader = csv.reader(data.splitlines())
        next(reader, None)
        for row in reader:
            try:
                self.total += int(row[1])
            except ValueError:
                raise ValueError('Distribution resources must only contain integers in the second column.')
            self.indices.append(self.total)
            self.values.append(row[0])

    def generate(self) -> str:
        """ Generates a random value, weighted by the known distribution
        """
        target = random.randint(0, self.total - 1)
        return self.values[bisect.bisect_left(self.indices, target)]
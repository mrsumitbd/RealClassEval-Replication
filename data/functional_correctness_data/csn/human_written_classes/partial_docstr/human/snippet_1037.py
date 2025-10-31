import pandas as pd

class DataFrameBuilder:

    def __init__(self):
        self.rows = []

    def add_row(self, row_data: dict):
        """Adds a new row to the DataFrame.

        Parameters:
            row_data (dict): Key-value pairs representing column names and their values for the row.
        """
        self.rows.append(row_data)

    def build(self) -> pd.DataFrame:
        """Constructs the DataFrame from the accumulated rows.

        Returns:
            A pandas DataFrame containing all the added rows.
        """
        return pd.DataFrame(self.rows)
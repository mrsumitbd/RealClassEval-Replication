
import os
import pandas as pd
import numpy as np


class _TPCDataGenerator:

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self.row_group_size = self.target_row_group_size_mb * \
            1024 * 1024  # Convert MB to bytes

    def run(self):
        if not self.target_mount_folder_path:
            raise ValueError("target_mount_folder_path must be specified")

        os.makedirs(self.target_mount_folder_path, exist_ok=True)

        # Example data generation for TPC-H table 'customer'
        num_rows = 150000 * self.scale_factor
        customer_data = self._generate_customer_data(num_rows)

        # Save to parquet with specified row group size
        file_path = os.path.join(
            self.target_mount_folder_path, 'customer.parquet')
        customer_data.to_parquet(file_path, row_group_size=self.row_group_size)

    def _generate_customer_data(self, num_rows):
        np.random.seed(0)  # For reproducibility
        customer_id = np.arange(1, num_rows + 1)
        cust_name = [f'Customer_{i}' for i in customer_id]
        address = [f'Address_{i}' for i in customer_id]
        nation_key = np.random.randint(1, 26, num_rows)  # Assuming 25 nations
        phone = [f'Phone_{i}' for i in customer_id]
        acct_bal = np.random.uniform(1000, 100000, num_rows)
        mkt_segment = np.random.choice(
            ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'MACHINERY', 'HOUSEHOLD'], num_rows)
        comment = [f'Comment_{i}' for i in customer_id]

        customer_df = pd.DataFrame({
            'C_CUST_KEY': customer_id,
            'C_NAME': cust_name,
            'C_ADDRESS': address,
            'C_NATIONKEY': nation_key,
            'C_PHONE': phone,
            'C_ACCTBAL': acct_bal,
            'C_MKTSEGMENT': mkt_segment,
            'C_COMMENT': comment
        })

        return customer_df

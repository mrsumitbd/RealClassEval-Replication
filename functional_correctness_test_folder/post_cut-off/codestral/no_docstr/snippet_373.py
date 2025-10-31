
import os
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from datetime import datetime, timedelta


class _TPCDataGenerator:

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):

        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self.row_group_size = target_row_group_size_mb * \
            1024 * 1024 // 8  # Assuming 8 bytes per row

    def run(self):

        if self.target_mount_folder_path is None:
            self.target_mount_folder_path = os.getcwd()

        # Generate and save data for each table
        self._generate_and_save_customer()
        self._generate_and_save_lineitem()
        self._generate_and_save_nation()
        self._generate_and_save_orders()
        self._generate_and_save_part()
        self._generate_and_save_partsupp()
        self._generate_and_save_region()
        self._generate_and_save_supplier()

    def _generate_and_save_customer(self):

        # Generate customer data
        customer_data = self._generate_customer_data()

        # Save customer data to parquet file
        self._save_to_parquet(customer_data, 'customer')

    def _generate_customer_data(self):

        # Generate customer data based on scale factor
        num_customers = self.scale_factor * 150000

        # Generate customer data
        customer_data = {
            'c_custkey': np.arange(num_customers, dtype=np.int32),
            'c_name': np.random.choice(['Customer' + str(i) for i in range(num_customers)], size=num_customers),
            'c_address': np.random.choice(['Address' + str(i) for i in range(num_customers)], size=num_customers),
            'c_nationkey': np.random.randint(0, 25, size=num_customers, dtype=np.int32),
            'c_phone': np.random.choice(['Phone' + str(i) for i in range(num_customers)], size=num_customers),
            'c_acctbal': np.random.uniform(0, 10000, size=num_customers),
            'c_mktsegment': np.random.choice(['BUILDING', 'AUTOMOBILE', 'MACHINERY', 'HOUSEHOLD', 'FURNITURE'], size=num_customers),
            'c_comment': np.random.choice(['Comment' + str(i) for i in range(num_customers)], size=num_customers)
        }

        return customer_data

    def _generate_and_save_lineitem(self):

        # Generate lineitem data
        lineitem_data = self._generate_lineitem_data()

        # Save lineitem data to parquet file
        self._save_to_parquet(lineitem_data, 'lineitem')

    def _generate_lineitem_data(self):

        # Generate lineitem data based on scale factor
        num_lineitems = self.scale_factor * 6001215

        # Generate lineitem data
        lineitem_data = {
            'l_orderkey': np.random.randint(0, self.scale_factor * 1500000, size=num_lineitems, dtype=np.int32),
            'l_partkey': np.random.randint(0, self.scale_factor * 200000, size=num_lineitems, dtype=np.int32),
            'l_suppkey': np.random.randint(0, self.scale_factor * 10000, size=num_lineitems, dtype=np.int32),
            'l_linenumber': np.random.randint(1, 8, size=num_lineitems, dtype=np.int32),
            'l_quantity': np.random.uniform(1, 50, size=num_lineitems),
            'l_extendedprice': np.random.uniform(1, 100000, size=num_lineitems),
            'l_discount': np.random.uniform(0, 0.1, size=num_lineitems),
            'l_tax': np.random.uniform(0, 0.08, size=num_lineitems),
            'l_returnflag': np.random.choice(['A', 'N', 'R'], size=num_lineitems),
            'l_linestatus': np.random.choice(['F', 'O'], size=num_lineitems),
            'l_shipdate': np.random.choice([datetime(1992, 1, 1) + timedelta(days=i) for i in range(2557)], size=num_lineitems),
            'l_commitdate': np.random.choice([datetime(1992, 1, 1) + timedelta(days=i) for i in range(2557)], size=num_lineitems),
            'l_receiptdate': np.random.choice([datetime(1992, 1, 1) + timedelta(days=i) for i in range(2557)], size=num_lineitems),
            'l_shipinstruct': np.random.choice(['DELIVER IN PERSON', 'COLLECT COD', 'NONE', 'TAKE BACK RETURN'], size=num_lineitems),
            'l_shipmode': np.random.choice(['TRUCK', 'SHIP', 'MAIL', 'RAIL', 'FOB', 'AIR'], size=num_lineitems),
            'l_comment': np.random.choice(['Comment' + str(i) for i in range(num_lineitems)], size=num_lineitems)
        }

        return lineitem_data

    def _generate_and_save_nation(self):

        # Generate nation data
        nation_data = self._generate_nation_data()

        # Save nation data to parquet file
        self._save_to_parquet(nation_data, 'nation')

    def _generate_nation_data(self):

        # Generate nation data
        nation_data = {
            'n_nationkey': np.arange(25, dtype=np.int32),
            'n_name': np.array(['ALGERIA', 'ARGENTINA', 'BRAZIL', 'CANADA', 'EGYPT', 'ETHIOPIA', 'FRANCE', 'GERMANY', 'INDIA', 'INDONESIA', 'IRAN', 'IRAQ', 'JAPAN', 'JORDAN', 'KENYA', 'MOROCCO', 'MOZAMBIQUE', 'PERU', 'CHINA', 'ROMANIA', 'SAUDI ARABIA', 'VIETNAM', 'RUSSIA', 'UNITED KINGDOM', 'UNITED STATES']),
            'n_regionkey': np.random.randint(0, 5, size=25, dtype=np.int32),
            'n_comment': np.random.choice(['Comment' + str(i) for i in range(25)], size=25)
        }

        return nation_data

    def _generate_and_save_orders(self):

        # Generate orders data
        orders_data = self._generate_orders_data()

        # Save orders data to parquet file
        self._save_to_parquet(orders_data, 'orders')

    def _generate_orders_data(self):

        # Generate orders data based on scale factor
        num_orders = self.scale_factor * 1500000

        # Generate orders data
        orders_data = {
            'o_orderkey': np.arange(num_orders, dtype=np.int32),
            'o_custkey': np.random.randint(0, self.scale_factor * 150000, size=num_orders, dtype=np.int32),
            'o_orderstatus': np.random.choice(['F', 'O', 'P'], size=num_orders),
            'o_totalprice': np.random.uniform(1, 1000000, size=num_orders),
            'o_orderdate': np.random.choice([datetime(1992, 1, 1) + timedelta(days=i) for i in range(2557)], size=num_orders),
            'o_orderpriority': np.random.choice(['1-URGENT', '2-HIGH', '3-MEDIUM', '4-NOT SPECIFIED', '5-LOW'], size=num_orders),
            'o_clerk': np.random.choice(['Clerk' + str(i) for i in range(num_orders)], size=num_orders),
            'o_shippriority': np.random.randint(0, 1, size=num_orders, dtype=np.int32),
            'o_comment': np.random.choice(['Comment' + str(i) for i in range(num_orders)], size=num_orders)
        }

        return orders_data

    def _generate_and_save_part(self):

        # Generate part data
        part_data = self._generate_part_data()

        # Save part data to parquet file
        self._save_to_parquet(part_data, 'part')

    def _generate_part_data(self):

        # Generate part data based on scale factor
        num_parts = self.scale_factor * 200000

        # Generate part data
        part_data = {
            'p_partkey': np.arange(num_parts, dtype=np.int32),
            'p_name': np.random.choice(['Part' + str(i) for i in range(num_parts)], size=num_parts),
            'p_mfgr': np.random.choice(['Manufacturer' + str(i) for i in range(num_parts)], size=num_parts),
            'p_brand': np.random.choice(['Brand' + str(i) for i in range(num_parts)], size=num_parts),
            'p_type': np.random.choice(['Type' + str(i) for i in range(num_parts)], size=num_parts),
            'p_size': np.random.randint(1, 50, size=num_parts, dtype=np.int32),
            'p_container': np.random.choice(['SM CASE', 'SM BOX', 'SM PACK', 'SM PKG', 'LG CASE', 'LG BOX', 'LG PACK', 'LG PKG', 'JUMBO CASE', 'JUMBO BOX', 'JUMBO PACK', 'JUMBO PKG'], size=num_parts),
            'p_retailprice': np.random.uniform(900, 2090, size=num_parts),
            'p_comment': np.random.choice(['Comment' + str(i) for i in range(num_parts)], size=num_parts)
        }

        return part_data

    def _generate_and_save_partsupp(self):

        # Generate partsupp data
        partsupp_data = self._generate_partsupp_data()

        # Save partsupp data to parquet file
        self._save_to_parquet(partsupp_data, 'partsupp')

    def _generate_partsupp_data(self):

        # Generate partsupp data based on scale factor
        num_partsupp = self.scale_factor * 800000

        # Generate partsupp data
        partsupp_data = {
            'ps_partkey': np.random.randint(0, self.scale_factor * 200000, size=num_partsupp, dtype=np.int32),
            'ps_suppkey': np.random.randint(0, self.scale_factor * 10000, size=num_partsupp, dtype=np.int32),
            'ps_availqty': np.random.randint(1, 9999, size=num_partsupp, dtype=np.int32),
            'ps_supplycost': np.random.uniform(1, 1000, size=num_partsupp),
            'ps_comment': np.random.choice(['Comment' + str(i) for i in range(num_partsupp)], size=num_partsupp)
        }

        return partsupp_data

    def _generate_and_save_region(self):

        # Generate region data
        region_data = self._generate_region_data()

        # Save region data to parquet file
        self._save_to_parquet(region_data, 'region')

    def _generate_region_data(self):

        # Generate region data
        region_data = {
            'r_regionkey': np.arange(5, dtype=np.int32),
            'r_name': np.array(['AFRICA', 'AMERICA', 'ASIA', 'EUROPE', 'MIDDLE EAST']),
            'r_comment': np.random.choice(['Comment' + str(i) for i in range(5)], size=5)
        }

        return region_data

    def _generate_and_save_supplier(self):

        # Generate supplier data
        supplier_data = self._generate_supplier_data()

        # Save supplier data to parquet file
        self._save_to_parquet(supplier_data, 'supplier')

    def _generate_supplier_data(self):

        # Generate supplier data based on scale factor
        num_suppliers = self.scale_factor * 10000

        # Generate supplier data
        supplier_data = {
            's_suppkey': np.arange(num_suppliers, dtype=np.int32),
            's_name': np.random.choice(['Supplier' + str(i) for i in range(num_suppliers)], size=num_suppliers),
            's_address': np.random.choice(['Address' + str(i) for i in range(num_suppliers)], size=num_suppliers),
            's_nationkey': np.random.randint(0, 25, size=num_suppliers, dtype=np.int32),
            's_phone': np.random.choice(['Phone' + str(i) for i in range(num_suppliers)], size=num_suppliers),
            's_acctbal': np.random.uniform(0, 10000, size=num_suppliers),
            's_comment': np.random.choice(['Comment' + str(i) for i in range(num_suppliers)], size=num_suppliers)
        }

        return supplier_data

    def _save_to_parquet(self, data: dict, table_name: str):

        # Convert data to pyarrow table
        table = pa.Table.from_pydict(data)

        # Create output file path
        output_file_path = os.path.join(
            self.target_mount_folder_path, f'{table_name}.parquet')

        # Write table to parquet file
        pq.write_table(table, output_file_path,
                       row_group_size=self.row_group_size)

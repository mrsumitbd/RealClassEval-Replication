class UserDatabaseContext:

    def __init__(self, paths):
        self.redundant_call = paths == loaded_user_db_paths
        if not self.redundant_call:
            self.old_loaded_user_dbs = loaded_user_dbs.copy()
            self.old_loaded_user_db_paths = loaded_user_db_paths.copy()
            set_user_chemical_property_databases(paths)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global loaded_user_dbs, loaded_user_db_paths
        if not self.redundant_call:
            loaded_user_dbs = self.old_loaded_user_dbs
            loaded_user_db_paths = self.old_loaded_user_db_paths
        return exc_type is None
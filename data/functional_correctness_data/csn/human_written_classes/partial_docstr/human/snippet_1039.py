from zipfile import ZipFile
import pandas as pd
import os

class OPFResults:

    def __init__(self):
        self.status = None
        self.solution_time = None
        self.solver = None
        self.lines_t = LineVariables()
        self.slack_generator_t = pd.DataFrame()
        self.heat_storage_t = HeatStorage()
        self.hv_requirement_slacks_t = pd.DataFrame()
        self.grid_slacks_t = GridSlacks()
        self.overlying_grid = pd.DataFrame()
        self.battery_storage_t = BatteryStorage()

    def to_csv(self, directory, attributes=None):
        """
        Exports OPF results data to csv files.

        The following attributes can be exported:

        * 'lines_t' : The results of the three variables in attribute
          :py:attr:`~lines_t` are saved to `lines_t_p.csv`, `lines_t_p.csv`, and
          `lines_t_ccm.csv`.
        * 'slack_generator_t' : Attribute :py:attr:`~slack_generator_t` is saved to
          `slack_generator_t.csv`.
        * 'heat_storage_t' : The results of the two variables in attribute
          :py:attr:`~heat_storage_t` are saved to `heat_storage_t_p.csv` and
          `heat_storage_t_e.csv`.
        * 'hv_requirement_slacks_t' : Attribute :py:attr:`~hv_requirement_slacks_t` is
          saved to `hv_requirement_slacks_t.csv`.
        * 'grid_slacks_t' : The results of the five variables in attribute
          :py:attr:`~grid_slacks_t` are saved to `dispatchable_gen_crt.csv`,
          `non_dispatchable_gen_crt.csv`, `load_shedding.csv`, `cp_load_shedding.csv`
          and `hp_load_shedding.csv`.
        * 'overlying_grid' : Attribute :py:attr:`~overlying_grid` is saved to
          `overlying_grid.csv`.

        Parameters
        ----------
        directory : str
            Path to save OPF results data to.
        attributes : list(str) or None
            List of attributes to export. See above for attributes that can be exported.
            If None, all specified attributes are exported. Default: None.

        """
        os.makedirs(directory, exist_ok=True)
        attrs_file_names = _get_matching_dict_of_attributes_and_file_names()
        if attributes is None:
            attributes = list(attrs_file_names.keys())
        for attr in attributes:
            file = attrs_file_names[attr]
            df = getattr(self, attr)
            if attr in ['lines_t', 'heat_storage_t', 'grid_slacks_t', 'battery_storage_t']:
                for variable in file.keys():
                    if variable in df._attributes() and (not getattr(df, variable).empty):
                        path = os.path.join(directory, file[variable])
                        getattr(df, variable).to_csv(path)
            elif not df.empty:
                path = os.path.join(directory, file)
                df.to_csv(path)

    def from_csv(self, data_path, from_zip_archive=False):
        """
        Restores OPF results from csv files.

        Parameters
        ----------
        data_path : str
            Path to OPF results csv files.
        from_zip_archive : bool, optional
            Set True if data is archived in a zip archive. Default: False.

        """
        attrs = _get_matching_dict_of_attributes_and_file_names()
        if from_zip_archive:
            zip = ZipFile(data_path)
            files = zip.namelist()
            attrs = {k: f'opf_results/{v}' if isinstance(v, str) else {k2: f'opf_results/{v2}' for k2, v2 in v.items()} for k, v in attrs.items()}
        else:
            files = os.listdir(data_path)
        attrs_to_read = {k: v for k, v in attrs.items() if isinstance(v, str) and v in files or (isinstance(v, dict) and any([_ in files for _ in v.values()]))}
        for attr, file in attrs_to_read.items():
            if attr in ['lines_t', 'heat_storage_t', 'grid_slacks_t', 'battery_storage_t']:
                for variable, file_name in file.items():
                    if file_name in files:
                        if from_zip_archive:
                            with zip.open(file_name) as f:
                                setattr(getattr(self, attr), variable, pd.read_csv(f, index_col=0, parse_dates=True))
                        else:
                            path = os.path.join(data_path, file_name)
                            setattr(getattr(self, attr), variable, pd.read_csv(path, index_col=0, parse_dates=True))
            else:
                if from_zip_archive:
                    with zip.open(file) as f:
                        df = pd.read_csv(f, index_col=0, parse_dates=True)
                else:
                    path = os.path.join(data_path, file)
                    df = pd.read_csv(path, index_col=0, parse_dates=True)
                setattr(self, attr, df)
        if from_zip_archive:
            zip.close()
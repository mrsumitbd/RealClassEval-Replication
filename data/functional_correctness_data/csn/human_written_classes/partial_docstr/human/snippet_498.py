import os

class FileStruct:

    def __init__(self, audio_file):
        """Creates the entire file structure given the audio file."""
        self.ds_path = os.path.dirname(os.path.dirname(audio_file))
        self.audio_file = audio_file
        self.est_file = self._get_dataset_file(ds_config.estimations_dir, ds_config.estimations_ext)
        self.features_file = self._get_dataset_file(ds_config.features_dir, ds_config.features_ext)
        self.ref_file = self._get_dataset_file(ds_config.references_dir, ds_config.references_ext)

    def _get_dataset_file(self, dir, ext):
        """Gets the desired dataset file."""
        audio_file_ext = '.' + self.audio_file.split('.')[-1]
        base_file = os.path.basename(self.audio_file).replace(audio_file_ext, ext)
        return os.path.join(self.ds_path, dir, base_file)

    def __repr__(self):
        """Prints the file structure."""
        return 'FileStruct(\n\tds_path=%s,\n\taudio_file=%s,\n\test_file=%s,\n\tfeatures_file=%s,\n\tref_file=%s\n)' % (self.ds_path, self.audio_file, self.est_file, self.features_file, self.ref_file)
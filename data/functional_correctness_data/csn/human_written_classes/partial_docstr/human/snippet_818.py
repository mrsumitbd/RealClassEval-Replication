class VolumeDetector:
    type = None
    special = False

    def detect(self, volume_system, vstype='detect'):
        """Finds and mounts all volumes based on parted.

        :param VolumeSystem volume_system: The volume system.
        """
        raise NotImplementedError()

    def _format_index(self, volume_system, idx):
        """Returns a formatted index given the disk index idx."""
        if volume_system.parent.index is not None:
            return '{0}.{1}'.format(volume_system.parent.index, idx)
        else:
            return str(idx)
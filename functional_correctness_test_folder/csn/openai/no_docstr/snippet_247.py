
class Merger:
    """
    Utility class for merging configuration dictionaries.
    """

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        """
        Merge the `extends` dictionary into the `target` dictionary.

        Parameters
        ----------
        target : dict
            The dictionary that will receive the merged values.
        extends : dict
            The dictionary whose values will be merged into `target`.
        inherit_key : str, optional
            Key used in `extends` to indicate whether inheritance should occur.
        inherit : bool, optional
            If True, perform the merge. If False, return `target` unchanged.
            If None, the value of `extends[inherit_key]` (if present) is used.

        Returns
        -------
        dict
            The merged dictionary (the same object as `target`).
        """
        if not isinstance(target, dict) or not isinstance(extends, dict):
            return target

        # Determine whether to inherit
        if inherit is None:
            inherit = extends.get(inherit_key, False)

        if not inherit:
            return target

        for key, value in extends.items():
            if key == inherit_key:
                continue

            if key in target:
                tgt_val = target[key]
                # Recursive merge for nested dictionaries
                if isinstance(tgt_val, dict) and isinstance(value, dict):
                    target[key] = self.merge_extends(
                        tgt_val, value, inherit_key, inherit=True)
                # Concatenate lists
                elif isinstance(tgt_val, list) and isinstance(value, list):
                    target[key] = tgt_val + value
                # Override other types
                else:
                    target[key] = value
            else:
                target[key] = value

        return target

    def merge_sources(self, datas):
        """
        Merge a list of dictionaries into a single dictionary.

        Parameters
        ----------
        datas : list of dict
            The list of dictionaries to merge. Later dictionaries override earlier ones.

        Returns
        -------
        dict
            The merged dictionary.
        """
        result = {}
        for data in datas:
            if isinstance(data, dict):
                result = self.merge_extends(result, data, inherit=True)
        return result

    def merge_configs(self, config, datas):
        """
        Merge a configuration dictionary with a list of source dictionaries.

        Parameters
        ----------
        config : dict
            The base configuration dictionary.
        datas : list of dict
            The list of source dictionaries to merge into `config`.

        Returns
        -------
        dict
            The merged configuration dictionary.
        """
        if not isinstance(config, dict):
            config = {}

        merged_sources = self.merge_sources(datas)
        return self.merge_extends(config, merged_sources, inherit=True)

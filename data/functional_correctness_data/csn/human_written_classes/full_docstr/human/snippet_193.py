class CkClass:
    """
    Base class for CK_* classes
    """
    flags_dict = {}
    fields = {}
    flags = 0

    def flags2text(self):
        """
        parse the `self.flags` field and create a list of `CKF_*` strings
        corresponding to bits set in flags

        :return: a list of strings
        :rtype: list
        """
        r = []
        for k, v in self.flags_dict.items():
            if self.flags & k:
                r.append(v)
        return r

    def state2text(self):
        """
        Dummy method. Will be overwriden if necessary
        """
        return ''

    def to_dict(self):
        """
        convert the fields of the object into a dictionnary
        """
        dico = {}
        for field in self.fields:
            if field == 'flags':
                dico[field] = self.flags2text()
            elif field == 'state':
                dico[field] = self.state2text()
            else:
                dico[field] = self.__dict__[field]
        return dico

    def __str__(self):
        """
        text representation of the object
        """
        dico = self.to_dict()
        lines = []
        for key in sorted(dico.keys()):
            ck_type = self.fields[key]
            if ck_type == 'flags':
                flags = ', '.join(dico[key])
                lines.append(f'{key}: {flags}')
            elif ck_type == 'pair':
                p1, p2 = dico[key]
                lines.append(f'{key}: {p1}.{p2}')
            else:
                lines.append(f'{key}: {dico[key]}')
        return '\n'.join(lines)
class DelegationHelper:
    """
    Helper class for building committees/delegations from rep json data
    given dicts for equivalences and abbreviations
    """

    def __init__(self, equivs, abbrevs, committees=True):
        self.equivs = equivs
        self.abbrevs = abbrevs
        self.committees = committees

    def __call__(self, data):
        items = []
        start = data['mandat_debut']
        end = data.get('mandat_fin', None)
        if self.committees:
            gdata = (i['responsabilite'] for i in data['responsabilites'])
        else:
            gdata = [i['responsabilite'] for i in data['responsabilites']] + [j['responsabilite'] for j in data['groupes_parlementaires']]
        for g in gdata:
            orga = g['organisme']
            role = g['fonction']
            is_committee = orga.lower().startswith('commission') and (not (orga.lower().startswith(u'commission spéciale') or orga.lower().startswith(u"commission d'enquête")))
            if self.committees != is_committee:
                continue
            if orga in self.equivs:
                orga = self.equivs[orga]
            item = {'abbr': self.abbrevs[orga] if orga in self.abbrevs else '', 'name': orga, 'role': role, 'start': start}
            if end:
                item['end'] = end
            items.append(item)
        return items
class CCLicense:

    @staticmethod
    def url(license):
        license = RIGHTS_ALIAS.get(license, license)
        if license in LICENSE_LIST_ALL:
            return INFO_ALL[LICENSE_LIST_ALL.index(license)][3]
        else:
            return ''

    @staticmethod
    def badge(license):
        if license == 'PD-US':
            return '/static/images/pdmark.png'
        elif license == 'CC0':
            return '/static/images/cc0.png'
        elif license == 'CC BY':
            return '/static/images/ccby.png'
        elif license == 'CC BY-NC-ND':
            return '/static/images/ccbyncnd.png'
        elif license == 'CC BY-NC-SA':
            return '/static/images/ccbyncsa.png'
        elif license == 'CC BY-NC':
            return '/static/images/ccbync.png'
        elif license == 'CC BY-SA':
            return '/static/images/ccbysa.png'
        elif license == 'CC BY-ND':
            return '/static/images/ccbynd.png'
        elif license == 'GFDL':
            return '/static/images/gfdl.png'
        elif license == 'LAL':
            return '/static/images/lal.png'
        else:
            return ''
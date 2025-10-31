from apidoc.object.source_dto import Version
from apidoc.object.source_dto import Root as ObjectRoot
from apidoc.object.source_dto import MultiVersion

class RootDto:
    """ Root Factory
    """

    def create_from_root(self, root_source):
        """Return a populated Object Root from dictionnary datas
        """
        root_dto = ObjectRoot()
        root_dto.configuration = root_source.configuration
        root_dto.versions = [Version(x) for x in root_source.versions.values()]
        for version in sorted(root_source.versions.values()):
            hydrator = Hydrator(version, root_source.versions, root_source.versions[version.name].types)
            for method in version.methods.values():
                hydrator.hydrate_method(root_dto, root_source, method)
            for type in version.types.values():
                hydrator.hydrate_type(root_dto, root_source, type)
        self.define_changes_status(root_dto)
        return root_dto

    def define_changes_status(self, root_dto):
        sorted_version = sorted(root_dto.versions)
        items = []
        for category in root_dto.method_categories:
            items = items + category.methods
        for category in root_dto.type_categories:
            items = items + category.types
        for item in items:
            new = False
            for version in sorted_version:
                if version.name not in item.changes_status.keys():
                    if new:
                        item.changes_status[version.name] = MultiVersion.Changes.deleted
                        new = False
                    else:
                        item.changes_status[version.name] = MultiVersion.Changes.none
                elif not new:
                    item.changes_status[version.name] = MultiVersion.Changes.new
                    new = True
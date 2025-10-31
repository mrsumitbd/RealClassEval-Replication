from typing import IO, Any, Optional, Union, cast

class EnumDefinition:
    """Prototype of a enum."""

    def __init__(self, name: str, values: list[str]):
        """Initialize enum definition with a name and possible values."""
        self.name = name
        self.values = values
        self.namespace, self.classname = split_name(name)
        self.namespace = safenamespacename(self.namespace)
        self.classname = safename(self.classname)

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        """Write enum definition to output."""
        namespace = ''
        if len(self.name.split('#')) == 2:
            namespace, classname = split_name(self.name)
            namespace = safenamespacename(namespace)
            classname = safename(classname)
            name = namespace + '::' + classname
        else:
            name = safename(self.name)
            classname = name
        if len(namespace) > 0:
            target.write(f'namespace {namespace} {{\n')
        target.write(f'enum class {classname} : unsigned int {{\n{ind}')
        target.write(f',\n{ind}'.join(map(safename, self.values)))
        target.write('\n};\n')
        target.write(f'inline auto to_string({classname} v) {{\n')
        target.write(f'{ind}static auto m = std::vector<std::string_view> {{\n')
        target.write(f'{ind}    "')
        target.write(f'",\n{ind}    "'.join(self.values))
        target.write(f'"\n{ind}}};\n')
        target.write(f'{ind}using U = std::underlying_type_t<{name}>;\n')
        target.write(f'{ind}return m.at(static_cast<U>(v));\n}}\n')
        if len(namespace) > 0:
            target.write('}\n')
        target.write(f'inline void to_enum(std::string_view v, {name}& out) {{\n')
        target.write(f'{ind}static auto m = std::map<std::string, {name}, std::less<>> {{\n')
        for v in self.values:
            target.write(f'{ind}{ind}{{{q(v)}, {name}::{safename(v)}}},\n')
        target.write(f'{ind}}};\n{ind}auto iter = m.find(v);\n')
        target.write(f'{ind}if (iter == m.end()) throw bool{{}};\n')
        target.write(f'{ind}out = iter->second;\n}}\n')
        target.write(f'namespace {common_namespace} {{\n')
        target.write(f'inline auto toYaml({name} v, [[maybe_unused]] ::{common_namespace}::store_config const& config) {{\n')
        target.write(f'{ind}auto n = YAML::Node{{std::string{{to_string(v)}}}};\n')
        target.write(f'{ind}if (config.generateTags) n.SetTag("{name}");\n')
        target.write(f'{ind}return n;\n}}\n')
        target.write(f'inline void fromYaml(YAML::Node n, {name}& out) {{\n')
        target.write(f'{ind}to_enum(n.as<std::string>(), out);\n}}\n')
        if len(self.values):
            target.write(f'template <> struct IsConstant<{name}> : std::true_type {{}};\n')
        target.write('}\n')
        target.write('\n')
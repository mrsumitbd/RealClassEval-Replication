from typing import IO, Any, Optional, Union, cast

class ClassDefinition:
    """Prototype of a class."""

    def __init__(self, name: str):
        """Initialize the class definition with a name."""
        self.fullName = name
        self.extends: list[dict[str, str]] = []
        self.specializationTypes: list[str] = []
        self.allfields: list[FieldDefinition] = []
        self.fields: list[FieldDefinition] = []
        self.abstract = False
        self.namespace, self.classname = split_name(name)
        self.namespace = safenamespacename(self.namespace)
        self.classname = safename(self.classname)

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        """Write forward declaration."""
        target.write(f'{fullInd}namespace {self.namespace} {{ struct {self.classname}; }}\n')

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        """Write definition of the class."""
        target.write(f'{fullInd}namespace {self.namespace} {{\n')
        target.write(f'{fullInd}struct {self.classname}')
        extends = list(map(safename2, self.extends))
        override = ''
        virtual = 'virtual '
        if len(self.extends) > 0:
            target.write(f'\n{fullInd}{ind}: ')
            target.write(f'\n{fullInd}{ind}, '.join(extends))
            override = ' override'
            virtual = ''
        target.write(' {\n')
        for field in self.fields:
            field.writeDefinition(target, fullInd + ind, ind, self.namespace)
        if self.abstract:
            target.write(f'{fullInd}{ind}virtual ~{self.classname}() = 0;\n')
        else:
            target.write(f'{fullInd}{ind}{virtual}~{self.classname}(){override} = default;\n')
        target.write(f'{fullInd}{ind}{virtual}auto toYaml([[maybe_unused]] {common_namespace}::store_config const& config) const -> YAML::Node{override};\n')
        target.write(f'{fullInd}{ind}{virtual}void fromYaml(YAML::Node const& n){override};\n')
        target.write(f'{fullInd}}};\n')
        target.write(f'{fullInd}}}\n\n')

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        """Write definition with implementation."""
        extends = list(map(safename2, self.extends))
        if self.abstract:
            target.write(f'{fullInd}inline {self.namespace}::{self.classname}::~{self.classname}() = default;\n')
        target.write(f'{fullInd}inline auto {self.namespace}::{self.classname}::toYaml([[maybe_unused]] ::{common_namespace}::store_config const& config) const -> YAML::Node {{\n{fullInd}{ind}using ::{common_namespace}::toYaml;\n{fullInd}{ind}auto n = YAML::Node{{}};\n{fullInd}{ind}if (config.generateTags) {{\n{fullInd}{ind}{ind}n.SetTag("{self.classname}");\n{fullInd}{ind}}}\n')
        for e in extends:
            target.write(f'{fullInd}{ind}n = mergeYaml(n, {e}::toYaml(config));\n')
        for field in self.fields:
            fieldname = safename(field.name)
            target.write(f'{fullInd}{ind}{{\n')
            target.write(f'{fullInd}{ind}{ind} auto member = toYaml(*{fieldname}, config);\n')
            if field.typeDSL:
                target.write(f'{fullInd}{ind}{ind} member = simplifyType(member, config);\n')
            target.write(f'{fullInd}{ind}{ind} member = convertListToMap(member, {q(field.mapSubject)}, {q(field.mapPredicate)}, config);\n')
            target.write(f'{fullInd}{ind}{ind}addYamlField(n, {q(field.name)}, member);\n')
            target.write(f'{fullInd}{ind}}}\n')
        target.write(f'{fullInd}{ind}return n;\n{fullInd}}}\n')
        functionname = f'{self.namespace}::{self.classname}::fromYaml'
        target.write(f'{fullInd}inline void {functionname}([[maybe_unused]] YAML::Node const& n) {{\n{fullInd}{ind}using ::{common_namespace}::fromYaml;\n')
        for e in extends:
            target.write(f'{fullInd}{ind}{e}::fromYaml(n);\n')
        for field in self.fields:
            fieldname = safename(field.name)
            expandType = ''
            if field.typeDSL:
                expandType = 'expandType'
            target.write(f'{fullInd}{ind}{{\n{fullInd}{ind}{ind}auto nodeAsList = convertMapToList(n[{q(field.name)}], {q(field.mapSubject)}, {q(field.mapPredicate)});\n{fullInd}{ind}{ind}auto expandedNode = {expandType}(nodeAsList);\n{fullInd}{ind}{ind}fromYaml(expandedNode, *{fieldname});\n{fullInd}{ind}}}\n')
        target.write(f'{fullInd}}}\n')
        if not self.abstract:
            e = f'::{self.namespace}::{self.classname}'
            target.write(f'namespace {common_namespace} {{\ntemplate <>\nstruct DetectAndExtractFromYaml<{e}> {{\n    auto operator()(YAML::Node const& n) const -> std::optional<{e}> {{\n        if (!n.IsDefined()) return std::nullopt;\n        if (!n.IsMap()) return std::nullopt;\n        auto res = {e}{{}};\n\n')
            for field in self.fields:
                fieldname = safename(field.name)
                target.write(f'        if constexpr (::{common_namespace}::IsConstant<decltype(res.{fieldname})::value_t>::value) try {{\n            fromYaml(n[{q(field.name)}], *res.{fieldname});\n            fromYaml(n, res);\n            return res;\n        }} catch(...) {{}}\n\n')
            target.write('        return std::nullopt;\n    }\n};\n}\n')
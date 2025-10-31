from textx.scoping import Postponed, get_included_models, remove_models_from_repositories
from textx.exceptions import TextXError, TextXSemanticError, TextXSyntaxError
from textx.const import MULT_ASSIGN_ERROR, MULT_ONE, MULT_ONEORMORE, MULT_OPTIONAL, MULT_ZEROORMORE, RULE_ABSTRACT, RULE_MATCH, UNKNOWN_OBJ_ERROR
from textx.scoping.providers import PlainName as DefaultScopeProvider

class ReferenceResolver:
    """
    Responsibility: store current model state before reference resolving.
    When all models are parsed, start resolving all references in a loop.
    """

    def __init__(self, parser, model, pos_crossref_list):
        self.parser = parser
        self.model = model
        self.pos_crossref_list = pos_crossref_list
        self.delayed_crossrefs = []

    def has_unresolved_crossrefs(self, obj, attr_name=None):
        """
        Args:
            obj: has this object unresolved crossrefs in its fields
            (non recursively)

        Returns:
            True (has unresolved crossrefs) or False (else)
        """
        if get_model(obj) != self.model:
            return get_model(obj)._tx_reference_resolver.has_unresolved_crossrefs(obj)
        else:
            for crossref_obj, attr, _ in self.parser._crossrefs:
                if crossref_obj is obj and (not attr_name or attr_name == attr.name):
                    return True
            return False

    def resolve_one_step(self):
        """
        Resolves model references.
        """
        metamodel = self.parser.metamodel
        current_crossrefs = self.parser._crossrefs
        new_crossrefs = []
        self.delayed_crossrefs = []
        resolved_crossref_count = 0
        default_scope = DefaultScopeProvider()
        for obj, attr, crossref in current_crossrefs:
            if get_model(obj) == self.model:
                attr_value = getattr(obj, attr.name)
                attr_refs = [obj.__class__.__name__ + '.' + attr.name, '*.' + attr.name, obj.__class__.__name__ + '.*', '*.*']
                if crossref.scope_provider is not None:
                    resolved = crossref.scope_provider(obj, attr, crossref)
                else:
                    for attr_ref in attr_refs:
                        if attr_ref in metamodel.scope_providers:
                            if self.parser.debug:
                                self.parser.dprint(f' FOUND {attr_ref}')
                            resolved = metamodel.scope_providers[attr_ref](obj, attr, crossref)
                            break
                    else:
                        resolved = default_scope(obj, attr, crossref)
                if resolved is not None and type(resolved) is not Postponed and metamodel.textx_tools_support:
                    self.pos_crossref_list.append(RefRulePosition(name=crossref.obj_name, ref_pos_start=crossref.position, ref_pos_end=crossref.position + len(resolved.name), def_file_name=get_model(resolved)._tx_filename, def_pos_start=resolved._tx_position, def_pos_end=resolved._tx_position_end))
                if resolved is None and metamodel.builtins and (crossref.obj_name in metamodel.builtins):
                    from textx import textx_isinstance
                    if textx_isinstance(metamodel.builtins[crossref.obj_name], crossref.cls):
                        resolved = metamodel.builtins[crossref.obj_name]
                if resolved is None:
                    line, col = self.parser.pos_to_linecol(crossref.position)
                    raise TextXSemanticError(message=f'Unknown object "{crossref.obj_name}" of class "{crossref.cls.__name__}"', line=line, col=col, err_type=UNKNOWN_OBJ_ERROR, expected_obj_cls=crossref.cls, filename=self.model._tx_filename)
                if type(resolved) is Postponed:
                    self.delayed_crossrefs.append((obj, attr, crossref))
                    new_crossrefs.append((obj, attr, crossref))
                else:
                    resolved_crossref_count += 1
                    if attr.mult in [MULT_ONEORMORE, MULT_ZEROORMORE]:
                        attr_value.append(resolved)
                    else:
                        setattr(obj, attr.name, resolved)
            else:
                new_crossrefs.append((obj, attr, crossref))
        self.parser._crossrefs = new_crossrefs
        return (resolved_crossref_count, self.delayed_crossrefs)
import ast

class ChainedFunctionTransformer:

    def visit_chain(self, node, depth=1):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and isinstance(node.value.func.value, ast.Call):
            call_node = node.value
            temp_var_id = '__chain_tmp_{}'.format(depth)
            unvisited_inner_call = ast.Assign(targets=[ast.Name(id=temp_var_id, ctx=ast.Store())], value=call_node.func.value)
            ast.copy_location(unvisited_inner_call, node)
            inner_calls = self.visit_chain(unvisited_inner_call, depth + 1)
            for inner_call_node in inner_calls:
                ast.copy_location(inner_call_node, node)
            outer_call = self.generic_visit(type(node)(value=ast.Call(func=ast.Attribute(value=ast.Name(id=temp_var_id, ctx=ast.Load()), attr=call_node.func.attr, ctx=ast.Load()), args=call_node.args, keywords=call_node.keywords), **{field: value for field, value in ast.iter_fields(node) if field != 'value'}))
            ast.copy_location(outer_call, node)
            ast.copy_location(outer_call.value, node)
            ast.copy_location(outer_call.value.func, node)
            return [*inner_calls, outer_call]
        else:
            return [self.generic_visit(node)]

    def visit_Assign(self, node):
        return self.visit_chain(node)

    def visit_Return(self, node):
        return self.visit_chain(node)
import ast

class IfExpTransformer:
    """Goes through module and function bodies, adding extra Assign nodes due to IfExp expressions."""

    def visit_body(self, nodes):
        new_nodes = []
        count = 0
        for node in nodes:
            rewriter = IfExpRewriter(count)
            possibly_transformed_node = rewriter.visit(node)
            if rewriter.assignments:
                new_nodes.extend(rewriter.assignments)
                count += len(rewriter.assignments)
            new_nodes.append(possibly_transformed_node)
        return new_nodes

    def visit_FunctionDef(self, node):
        transformed = ast.FunctionDef(name=node.name, args=node.args, body=self.visit_body(node.body), decorator_list=node.decorator_list, returns=node.returns)
        ast.copy_location(transformed, node)
        return self.generic_visit(transformed)

    def visit_Module(self, node):
        transformed = ast.Module(self.visit_body(node.body))
        ast.copy_location(transformed, node)
        return self.generic_visit(transformed)
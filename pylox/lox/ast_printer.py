from .expr import *

class AstPrinter(ExprVisitor):
    def print(this, expr: Expr):
        return expr.accept(this)
    
    def parenthesize(self, name: str, *exprs: Expr) -> str:
        exprs = [expr.accept(self) for expr in exprs]
        return f'({name} {" ".join(exprs)})'
    
    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self.parenthesize('group', expr.expression)
    
    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value == None: return 'nil'
        if expr.value == True: return 'true'
        if expr.value == False: return 'false'
        return str(expr.value)
    
    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)
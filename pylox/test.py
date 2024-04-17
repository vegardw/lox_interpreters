from lox.expr import *
from lox.ast_printer import *
from lox.token import *

expression = BinaryExpr(
    UnaryExpr(
        Token(TokenType.MINUS, '-', None, 1),
        LiteralExpr(123)
    ),
    Token(TokenType.STAR, '*', None, 1),
    GroupingExpr(
        LiteralExpr(45.67)
    )
)

print(AstPrinter().print(expression))
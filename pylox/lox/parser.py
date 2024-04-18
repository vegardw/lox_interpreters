from .token import Token, TokenType
from .expr import *
from .lox import parser_error
from typing import List

class Parser:
    class ParseError(RuntimeError):
        pass

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except self.ParseError:
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)

        return expr
    
    def comparison(self)->Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)

        return expr
    
    def term(self)->Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)

        return expr
    
    def factor(self)->Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr,operator,right)

        return expr
    
    def unary(self)->Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)
        
        return self.primary()
    
    def primary(self)->Expr:
        if self.match(TokenType.FALSE) : return LiteralExpr(False)
        if self.match(TokenType.TRUE) : return LiteralExpr(True)
        if self.match(TokenType.NIL) : return LiteralExpr(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)
        
        raise self.error(self.peek(), "Expect expression.")

    def consume(self, type: TokenType, message: str)->Token:
        if self.check(type): return self.advance()

        raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str)->ParseError:
        parser_error(token,message)
        return self.ParseError()
    
    def synchronize(self)->None:
        self.advance()

        while not self.is_at_end():
            if self.peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ]:
                return
            
            self.advance()
        
    
    def match(self, *types: TokenType)->bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
            
        return False
    
    def check(self, type: TokenType)->bool:
        if self.is_at_end(): return False
        return self.peek().type == type

    def advance(self)->Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()
    
    def is_at_end(self)->bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self)->Token:
        return self.tokens[self.current]
    
    def previous(self)->Token:
        return self.tokens[self.current-1]
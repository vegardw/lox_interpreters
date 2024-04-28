from .token import Token, TokenType
from .expr import *
from .stmt import *
from .lox import parser_error
from typing import List

class Parser:
    class ParseError(RuntimeError):
        pass

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.FUN): return self.function_declaration("function")
            if self.match(TokenType.VAR): return self.var_declaration()

            return self.statement()
        except self.ParseError as e:
            self.synchronize()
            return None
    
    def statement(self) -> Stmt:
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            return BlockStmt(self.block())
        return self.expression_statement()
    
    def for_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if self.match(TokenType.SEMICOLON):
            pass
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()

        if increment != None:
            body = BlockStmt([
                body,
                ExpressionStmt(increment)
            ])

        if condition == None: condition = LiteralExpr(True)
        body = WhileStmt(condition,body)

        if initializer != None:
            body = BlockStmt([
                initializer,
                body
            ])

        return body


    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, else_branch)
    
    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)
    
    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(keyword, value)
    
    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")

        return VarStmt(name, initializer)
    
    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return WhileStmt(condition, body)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)
    
    def function_declaration(self, kind: str) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, f'Expect {kind} name.')
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    parser_error(self.peek(), "Can't have more than 255 parameters.")

                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

                if not self.match(TokenType.COMMA): break

        self.consume(TokenType.RIGHT_PAREN,  "Expect ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()

        return FunctionStmt(name, parameters, body)
    
    def block(self) -> List[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self) -> Expr:
        expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)
            
            parser_error(equals, "Invalid assignment target.")

        return expr
    
    def or_expr(self) -> Expr:
        expr = self.and_expr()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = LogicalExpr(expr, operator, right)

        return expr
    
    def and_expr(self) -> Expr:
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = LogicalExpr(expr, operator, right)

        return expr

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
        
        return self.call()
    
    def call(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr
    
    def finish_call(self, callee: Expr) -> Expr:
        arguments = []

        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    parser_error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return CallExpr(callee, paren, arguments)


    def primary(self)->Expr:
        if self.match(TokenType.FALSE) : return LiteralExpr(False)
        if self.match(TokenType.TRUE) : return LiteralExpr(True)
        if self.match(TokenType.NIL) : return LiteralExpr(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        
        if self.match(TokenType.IDENTIFIER):
            return VariableExpr(self.previous())
        
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